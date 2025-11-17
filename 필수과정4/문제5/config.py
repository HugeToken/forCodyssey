# config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./pyboard.db"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True 
    )

settings = Settings()