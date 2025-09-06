from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str
    bot_token: str = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"