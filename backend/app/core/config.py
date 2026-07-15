from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    HOST: str
    PORT: int

    DATABASE_URL: str

    OLLAMA_MODEL: str
    OLLAMA_HOST: str = "http://127.0.0.1:11434"

    FRONTEND_ORIGIN: str = "http://127.0.0.1:5173"

    class Config:
        env_file = ".env"


settings = Settings()
