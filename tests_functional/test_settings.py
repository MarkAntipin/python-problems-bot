from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    TEST_PG_HOST: str
    TEST_PG_USER: str
    TEST_PG_PASSWORD: str
    TEST_PG_DATABASE: str
    TEST_PG_PORT: int

    model_config = SettingsConfigDict(env_file='test_functional/.env', env_file_encoding='utf-8', extra='ignore')
