from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from ..auth import get_current_user
from ..db import get_client
from ..models import DailyLog, DailyLogCreate
from ..risk import calculate_training_load

router = APIRouter(prefix="/logs", tags=["logs"])


@router.post("", response_model=DailyLog, status_code=201)
def create_log(
    payload: DailyLogCreate, current_user: dict = get_current_user
) -> DailyLog:
    db = get_client()

    existing = (
        db.collection("logs")
        .where("user_id", "==", current_user["id"])
        .where("log_date", "==", payload.log_date)
        .limit(1)
        .stream()
    )
    existing_doc = next(existing, None)
    if existing_doc:
        raise HTTPException(status_code=400, detail="Log for date already exists")

    log_ref = db.collection("logs").document()
    training_load = calculate_training_load(
        payload.training_duration_min, payload.training_intensity
    )
    log_data = {
        "id": log_ref.id,
        "user_id": current_user["id"],
        "log_date": payload.log_date,
        "training_duration_min": payload.training_duration_min,
        "training_intensity": payload.training_intensity,
        "soreness": payload.soreness,
        "sleep_quality": payload.sleep_quality,
        "rest_day": payload.rest_day,
        "training_load": training_load,
        "created_at": datetime.now(timezone.utc),
    }
    log_ref.set(log_data)
    return DailyLog(**log_data)


@router.get("", response_model=list[DailyLog])
def list_logs(current_user: dict = get_current_user) -> list[DailyLog]:
    db = get_client()
    docs = (
        db.collection("logs")
        .where("user_id", "==", current_user["id"])
        .stream()
    )
    logs = [doc.to_dict() for doc in docs]
    logs.sort(key=lambda item: item["log_date"])
    return [DailyLog(**log) for log in logs]
