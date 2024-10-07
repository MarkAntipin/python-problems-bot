from pydantic import BaseModel, computed_field

from settings import app_settings


class Achievement(BaseModel):
    text: str
    title: str
    emoji: str
    name: str
    emoji_key: str

    @computed_field
    @property
    def emoji_image(self) -> str:
        return f'{app_settings.BACKEND_URL}/images/{self.emoji_key}.svg'
