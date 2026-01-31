from datetime import date, datetime

from fastapi import APIRouter

from ..auth import get_current_user
from ..db import get_client
from ..models import RiskSummary
from ..risk import summarize_risk

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def _normalize_log(log: dict) -> dict:
    log_date = log.get("log_date")
    if isinstance(log_date, datetime):
        log["log_date"] = log_date.date()
    return log


@router.get("", response_model=RiskSummary)
def get_recommendations(current_user: dict = get_current_user) -> RiskSummary:
    db = get_client()
    docs = (
        db.collection("logs")
        .where("user_id", "==", current_user["id"])
        .stream()
    )
    logs = [_normalize_log(doc.to_dict()) for doc in docs]
    logs.sort(key=lambda item: item["log_date"])
    return summarize_risk(logs, date.today())
