from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent

IMAGES_DIR = Path(BASE_DIR, 'images')

ENV_FILE = Path(BASE_DIR, '.env')
load_dotenv(ENV_FILE)

MAX_QUESTION_PER_DAY: int = 3


class PostgresSettings(BaseSettings):
    HOST: str
    USER: str
    PASSWORD: str
    DATABASE: str
    PORT: int

    @property
    def url(self) -> str:
        return f'postgres://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}'

    @property
    def url_for_persistence(self) -> str:
        return f'postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}'

    class Config:
        case_sensitive = False
        env_prefix = "PG_"


class BotSettings(BaseSettings):
    TOKEN: str

    class Config:
        case_sensitive = False


class TestSettings(BaseSettings):
    PG_HOST: str = 'localhost'
    PG_USER: str = 'python-problems-bot'
    PG_PASSWORD: str = 'python-problems-bot'
    PG_DATABASE: str = 'python-problems-bot'
    PG_PORT: int = 5432

    class Config:
        case_sensitive = False
        env_prefix = "TEST_"
