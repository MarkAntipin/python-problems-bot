from pydantic import BaseModel


class Achievement(BaseModel):
    text: str
    title: str
    emoji: str
    name: str
    emoji_key: str
