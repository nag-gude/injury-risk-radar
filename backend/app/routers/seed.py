from datetime import date, datetime, timedelta, timezone
import random
import uuid

from fastapi import APIRouter, Header, HTTPException

from ..auth import hash_password
from ..config import settings
from ..db import create_log, create_user, get_user_by_email

router = APIRouter(prefix="/seed", tags=["seed"])


@router.post("")
def seed_demo_data(x_seed_token: str | None = Header(default=None)) -> dict:
    if settings.seed_token and x_seed_token != settings.seed_token:
        raise HTTPException(status_code=401, detail="Invalid seed token")

    email = "demo@injuryriskradar.app"
    user = get_user_by_email(email)
    if not user:
        user = {
            "id": str(uuid.uuid4()),
            "email": email,
            "hashed_password": hash_password("DemoPass123!"),
            "role": "athlete",
            "sport": "Soccer",
            "age_group": "18-25",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        create_user(user)

    today = date.today()
    for offset in range(14, -1, -1):
        log_date = (today - timedelta(days=offset)).isoformat()
        training_duration = random.choice([30, 40, 50, 60, 75])
        intensity = random.choice([4, 5, 6, 7, 8])
        soreness = random.choice([2, 3, 4, 5, 6])
        sleep_quality = random.choice([5, 6, 7, 8, 9])
        rest_day = offset % 7 == 0
        if offset == 2:
            training_duration = 90
            intensity = 9

        log_data = {
            "id": str(uuid.uuid4()),
            "user_id": user["id"],
            "log_date": log_date,
            "training_duration_min": 0 if rest_day else training_duration,
            "training_intensity": 1 if rest_day else intensity,
            "soreness": soreness,
            "sleep_quality": sleep_quality,
            "rest_day": rest_day,
            "training_load": (0 if rest_day else training_duration * intensity),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        create_log(log_data)

    return {"status": "ok", "demo_email": email, "demo_password": "DemoPass123!"}
