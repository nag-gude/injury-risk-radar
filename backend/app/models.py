from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


Role = Literal["athlete", "coach", "parent"]
RiskLevel = Literal["Low", "Moderate", "High"]


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    role: Role
    sport: str
    age_group: str


class UserProfile(BaseModel):
    id: str
    email: EmailStr
    role: Role
    sport: str
    age_group: str
    created_at: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DailyLogCreate(BaseModel):
    log_date: date
    training_duration_min: int = Field(ge=0, le=600)
    training_intensity: int = Field(ge=1, le=10)
    soreness: int = Field(ge=1, le=10)
    sleep_quality: int = Field(ge=1, le=10)
    rest_day: bool = False


class DailyLog(DailyLogCreate):
    id: str
    user_id: str
    training_load: float
    created_at: datetime


class RiskSummary(BaseModel):
    risk_level: RiskLevel
    risk_score: float
    acute_load: float
    chronic_load: float
    load_ratio: float
    fatigue_score: float
    recommendations: list[str]


class DashboardSummary(BaseModel):
    today: RiskSummary
    logs: list[DailyLog]
