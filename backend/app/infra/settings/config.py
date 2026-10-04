from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="backend/.env"
    )

    db_user: str
    db_password: SecretStr
    db_port: int
    db_name: int
    db_host: str

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()
