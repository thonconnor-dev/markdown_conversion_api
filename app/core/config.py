from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL = 'postgresql+asyncpg://sethon:@localhost/markdowndb'