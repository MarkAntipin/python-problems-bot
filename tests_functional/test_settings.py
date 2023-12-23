from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    PG_HOST: str
    PG_USER: str
    PG_PASSWORD: str
    PG_DATABASE: str
    PG_PORT: int

    class Config:
        case_sensitive = False
        env_prefix = "TEST_"
