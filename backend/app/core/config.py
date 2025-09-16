from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./test.db"

    # JWT
    JWT_SECRET_KEY: str = "super-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRY_MINUTES: int = 60 * 24
    JWT_REFRESH_EXPIRY_MINUTES: int = 60 * 24 * 7

    # Configuration
    model_config = SettingsConfigDict(extra="ignore")


config = Config()
