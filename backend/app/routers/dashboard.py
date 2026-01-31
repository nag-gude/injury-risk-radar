from datetime import date, datetime

from fastapi import APIRouter

from ..auth import get_current_user
from ..db import get_client
from ..models import DailyLog, DashboardSummary
from ..risk import summarize_risk

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _normalize_log(log: dict) -> dict:
    log_date = log.get("log_date")
    if isinstance(log_date, datetime):
        log["log_date"] = log_date.date()
    return log


@router.get("", response_model=DashboardSummary)
def get_dashboard(current_user: dict = get_current_user) -> DashboardSummary:
    db = get_client()
    docs = (
        db.collection("logs")
        .where("user_id", "==", current_user["id"])
        .stream()
    )
    logs = [_normalize_log(doc.to_dict()) for doc in docs]
    logs.sort(key=lambda item: item["log_date"])

    today = date.today()
    summary = summarize_risk(logs, today)
    return DashboardSummary(
        today=summary,
        logs=[DailyLog(**log) for log in logs],
    )
