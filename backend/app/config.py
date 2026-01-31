from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Injury Risk Radar"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_exp_minutes: int = 60 * 24 * 7
    firestore_project: str | None = None


settings = Settings()
