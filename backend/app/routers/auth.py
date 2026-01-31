from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from ..auth import create_access_token, get_current_user, hash_password, verify_password
from ..db import get_client
from ..models import LoginRequest, TokenResponse, UserCreate, UserProfile

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserProfile, status_code=201)
def register_user(payload: UserCreate) -> UserProfile:
    db = get_client()
    existing = (
        db.collection("users")
        .where("email", "==", payload.email)
        .limit(1)
        .stream()
    )
    if any(True for _ in existing):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_ref = db.collection("users").document()
    user_data = {
        "id": user_ref.id,
        "email": payload.email,
        "hashed_password": hash_password(payload.password),
        "role": payload.role,
        "sport": payload.sport,
        "age_group": payload.age_group,
        "created_at": datetime.now(timezone.utc),
    }
    user_ref.set(user_data)
    return UserProfile(**user_data)


@router.post("/login", response_model=TokenResponse)
def login_user(payload: LoginRequest) -> TokenResponse:
    db = get_client()
    query = (
        db.collection("users")
        .where("email", "==", payload.email)
        .limit(1)
        .stream()
    )
    user_doc = next(query, None)
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = user_doc.to_dict()
    if not verify_password(payload.password, user.get("hashed_password", "")):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user["id"])
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserProfile)
def get_profile(current_user: dict = get_current_user) -> UserProfile:
    return UserProfile(**current_user)
