from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Mindo API"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    CORS_ORIGINS: str = "http://localhost:3000"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    GROQ_API_KEY: str = ""
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
