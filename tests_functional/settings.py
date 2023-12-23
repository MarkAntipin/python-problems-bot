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
    PG_HOST: str
    PG_USER: str
    PG_PASSWORD: str
    PG_DATABASE: str
    PG_PORT: int

    class Config:
        case_sensitive = False
        env_prefix = "TEST_"
