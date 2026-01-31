from datetime import datetime, timezone
import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.db import create_log, get_log_by_date, list_logs as list_user_logs
from app.models import DailyLog, DailyLogCreate
from app.risk import calculate_training_load

router = APIRouter(prefix="/logs", tags=["logs"])


@router.post("", response_model=DailyLog, status_code=201)
def create_log(
    payload: DailyLogCreate, current_user: dict = Depends(get_current_user)
) -> DailyLog:
    log_date_str = payload.log_date.isoformat()
    existing = get_log_by_date(current_user["id"], log_date_str)
    if existing:
        raise HTTPException(status_code=400, detail="Log for date already exists")

    training_load = calculate_training_load(
        payload.training_duration_min, payload.training_intensity
    )
    log_data = {
        "id": str(uuid.uuid4()),
        "user_id": current_user["id"],
        "log_date": log_date_str,
        "training_duration_min": payload.training_duration_min,
        "training_intensity": payload.training_intensity,
        "soreness": payload.soreness,
        "sleep_quality": payload.sleep_quality,
        "rest_day": payload.rest_day,
        "training_load": training_load,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    stored = create_log(log_data)
    if not stored:
        raise HTTPException(status_code=400, detail="Log for date already exists")
    return DailyLog(**log_data)


@router.get("", response_model=list[DailyLog])
def list_logs(current_user: dict = Depends(get_current_user)) -> list[DailyLog]:
    logs = list_user_logs(current_user["id"])
    logs.sort(key=lambda item: item["log_date"])
    return [DailyLog(**log) for log in logs]
