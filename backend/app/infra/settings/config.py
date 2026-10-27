from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import SecretStr, Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="backend/.env"
    )

    postgres_db: str
    postgres_user: str
    postgres_password: SecretStr
    postgres_host: str
    postgres_port: int

    youtube_transcript_api_key: str
    youtube_transcript_url: str

    secret_key: SecretStr 
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_hours: int = 744
    secure_refresh: int = Field(default=1, ge=0, le=1)

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

settings = Settings()