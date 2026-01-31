from datetime import datetime, timezone
import uuid

from fastapi import APIRouter, HTTPException, status

from ..auth import create_access_token, get_current_user, hash_password, verify_password
from ..db import create_user, get_user_by_email
from ..models import LoginRequest, TokenResponse, UserCreate, UserProfile

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserProfile, status_code=201)
def register_user(payload: UserCreate) -> UserProfile:
    existing = get_user_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        hashed_password = hash_password(payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    user_data = {
        "id": str(uuid.uuid4()),
        "email": payload.email,
        "hashed_password": hashed_password,
        "role": payload.role,
        "sport": payload.sport,
        "age_group": payload.age_group,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    stored = create_user(user_data)
    if not stored:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserProfile(**user_data)


@router.post("/login", response_model=TokenResponse)
def login_user(payload: LoginRequest) -> TokenResponse:
    user = get_user_by_email(payload.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user.get("hashed_password", "")):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user["id"])
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserProfile)
def get_profile(current_user: dict = get_current_user) -> UserProfile:
    return UserProfile(**current_user)
