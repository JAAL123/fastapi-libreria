from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Configuraciones de API

    PROJECT_NAME: str = "FastAPI Libreria"
    API_V1_STR: str = "/api/v1"

    # Configuraciones de base de datos

    DATABASE_URL: str

    # Configuraciones de seguridad

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Configuraciones de prestamos

    MAX_LOANS_PER_USER_ALLOWED: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
