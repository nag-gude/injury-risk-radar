from datetime import date, timedelta

from app.models import RiskSummary


def calculate_training_load(duration_min: int, intensity: int) -> float:
    return round(duration_min * intensity, 2)


def _avg(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def summarize_risk(logs: list[dict], today: date) -> RiskSummary:
    if not logs:
        return RiskSummary(
            risk_level="Low",
            risk_score=0.0,
            acute_load=0.0,
            chronic_load=0.0,
            load_ratio=0.0,
            fatigue_score=0.0,
            recommendations=["Add a log to calculate your injury risk."],
        )

    last_7_days = {
        (today - timedelta(days=offset)) for offset in range(0, 7)
    }
    last_28_days = {
        (today - timedelta(days=offset)) for offset in range(0, 28)
    }

    acute_loads = [
        log["training_load"]
        for log in logs
        if log["log_date"] in last_7_days
    ]
    chronic_loads = [
        log["training_load"]
        for log in logs
        if log["log_date"] in last_28_days
    ]
    acute_load = _avg(acute_loads)
    chronic_load = _avg(chronic_loads)
    load_ratio = round(acute_load / chronic_load, 2) if chronic_load else 0.0

    today_log = next(
        (log for log in logs if log["log_date"] == today), logs[-1]
    )
    soreness = today_log.get("soreness", 5)
    sleep_quality = today_log.get("sleep_quality", 5)
    rest_day = today_log.get("rest_day", False)

    fatigue_score = (
        (soreness / 10) * 0.45
        + ((10 - sleep_quality) / 10) * 0.45
        + (0.1 if not rest_day else 0.0)
    )

    load_risk = min(1.0, load_ratio / 1.5) if chronic_load else 0.5
    risk_score = round((load_risk * 0.6 + fatigue_score * 0.4) * 100, 2)

    if risk_score < 33:
        risk_level = "Low"
        recommendations = [
            "Keep a steady training routine and prioritize recovery habits.",
            "Maintain good sleep and hydration to support tissue repair.",
        ]
    elif risk_score < 66:
        risk_level = "Moderate"
        recommendations = [
            "Consider a lighter session or extra recovery today.",
            "Monitor soreness and sleep closely over the next 48 hours.",
        ]
    else:
        risk_level = "High"
        recommendations = [
            "Reduce training load and add a rest or low-intensity day.",
            "If symptoms persist, consult a qualified professional.",
        ]

    return RiskSummary(
        risk_level=risk_level,
        risk_score=risk_score,
        acute_load=round(acute_load, 2),
        chronic_load=round(chronic_load, 2),
        load_ratio=load_ratio,
        fatigue_score=round(fatigue_score * 100, 2),
        recommendations=recommendations,
    )
