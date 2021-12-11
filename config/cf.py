from os import environ

from logzero import loglevel
from pydantic import BaseModel


class AppConfig(BaseModel):
    APP_NAME: str = 'testPythonProject'
    STAGE: str = 'dev'
    LOG_LEVEL: int = 10

    MYSQL_URL: str

    FASTAPI_HOST: str = "0.0.0.0"
    FASTAPI_PORT: int = 2100

    ROUND_TIME: int = 600  # round time and step


def load_config() -> AppConfig:
    config = AppConfig(**environ)
    loglevel(level=config.LOG_LEVEL)
    return config


CONFIG = load_config()
