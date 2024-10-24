from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()
