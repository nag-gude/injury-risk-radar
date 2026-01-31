from datetime import date, datetime

from fastapi import APIRouter

from app.auth import get_current_user
from app.db import list_logs as list_user_logs
from app.models import RiskSummary
from app.risk import summarize_risk

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def _normalize_log(log: dict) -> dict:
    log_date = log.get("log_date")
    if isinstance(log_date, datetime):
        log["log_date"] = log_date.date()
    elif isinstance(log_date, str):
        log["log_date"] = date.fromisoformat(log_date)
    return log


@router.get("", response_model=RiskSummary)
def get_recommendations(current_user: dict = get_current_user) -> RiskSummary:
    logs = [_normalize_log(log) for log in list_user_logs(current_user["id"])]
    logs.sort(key=lambda item: item["log_date"])
    return summarize_risk(logs, date.today())
