from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = "FastAPI Libreria"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = (
        "postgresql://libreria_user:libreria_password@localhost:5432/libreria_db"
    )

    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
