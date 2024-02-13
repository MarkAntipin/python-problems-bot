from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent

IMAGES_DIR = Path(BASE_DIR, 'images')

ENV_FILE = Path(BASE_DIR, '.env')
load_dotenv(ENV_FILE)

MAX_QUESTION_PER_DAY: int = 3

WEB_APP_URL = 'https://localhost:8000/question/{question_id}/result/?return_type={return_type}'


class PostgresSettings(BaseSettings):
    HOST: str = 'localhost'
    USER: str = 'postgres'
    PASSWORD: str = 'postgres'
    DATABASE: str = 'python-problems-bot'
    PORT: int = 5432

    @property
    def url(self) -> str:
        return f'postgres://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}'

    @property
    def url_for_persistence(self) -> str:
        return f'postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}'

    model_config = SettingsConfigDict(env_file=ENV_FILE, case_sensitive=False, env_prefix="PG_")


class BotSettings(BaseSettings):
    TOKEN: str = '6605895101:AAEPjxsl0ORfNwawp4ZWhmGzA8sckj9ShZY'

    model_config = SettingsConfigDict(env_file=ENV_FILE, case_sensitive=False)


class TestSettings(BaseSettings):
    PG_HOST: str = 'localhost'
    PG_USER: str = 'python-problems-bot'
    PG_PASSWORD: str = 'python-problems-bot'
    PG_DATABASE: str = 'python-problems-bot'
    PG_PORT: int = 5432

    model_config = SettingsConfigDict(env_file=ENV_FILE, case_sensitive=False, env_prefix="TEST_")
