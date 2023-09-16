import datetime
from pathlib import Path

import dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent

IMAGES_DIR = Path(BASE_DIR, 'images')

ENV_FILE = Path(BASE_DIR, '.env')
dotenv.load_dotenv(ENV_FILE)

MOSCOW_TIME_DIFFERENCE = datetime.timedelta(hours=3)


class PostgresSettings(BaseSettings):
    HOST: str
    USER: str
    PASSWORD: str
    DATABASE: str
    PORT: int = 5432

    @property
    def url(self) -> str:
        return f'postgres://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}'

    @property
    def url_for_persistence(self) -> str:
        return f'postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}'

    class Config:
        case_sensitive = False
        env_prefix = "PG_"


class MongoSettings(BaseSettings):
    HOST: str
    USER: str
    PASSWORD: str
    DATABASE: str = 'admin'
    PORT: int = 27017

    @property
    def url(self) -> str:
        return (
            f'mongodb://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?retryWrites=true&w=majority'
        )

    class Config:
        case_sensitive = False
        env_prefix = "MONGO_"


class BotSettings(BaseSettings):
    TOKEN: str
    MAX_QUESTION_PER_DAY: int = 3

    class Config:
        case_sensitive = False


class TestSettings(BaseSettings):
    TELEGRAM_APP_ID: int
    TELEGRAM_APP_HASH: str
    TELETHON_SESSION: str
    BOT_NAME: str

    PG_HOST: str = 'localhost'
    PG_USER: str = 'python-problems-bot'
    PG_PASSWORD: str = 'python-problems-bot'
    PG_DATABASE: str = 'python-problems-bot'
    PG_PORT: int = 5436

    class Config:
        case_sensitive = False
        env_prefix = "TEST_"


bot_settings = BotSettings()
