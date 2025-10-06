from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://sethon:@localhost:5432/markdowndb"
    
settings = Settings()
