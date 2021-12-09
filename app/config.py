from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_USER: str = "Not loaded"
    DB_PASSWORD: str = "Not loaded"

    class Config:
        env_file = "app/secrets/.envapp"
