from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "job-radar"
    environment: str = "development"
    database_url: str = "sqlite+aiosqlite:///./job_radar.db"
    discord_webhook_url: str | None = None
    poll_intererval_minutes: int = 15

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

setting = Settings()