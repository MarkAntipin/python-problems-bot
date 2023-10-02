from enum import StrEnum
from enum import auto
from pathlib import Path

from settings import IMAGES_DIR


class ImageType(StrEnum):
    greeting = auto()


IMAGE_TYPE_TO_IMAGE_PATH = {
    ImageType.greeting: Path(IMAGES_DIR, 'greeting.png'),
}
