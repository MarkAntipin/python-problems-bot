from enum import StrEnum, auto
from pathlib import Path

from settings import IMAGES_DIR


class ImageType(StrEnum):
    greeting = auto()
    thank_you = auto()
    miss_you = auto()


IMAGE_TYPE_TO_IMAGE_PATH = {
    ImageType.greeting: Path(IMAGES_DIR, 'greeting.png'),
    ImageType.thank_you: Path(IMAGES_DIR, 'thank-you.png'),
    ImageType.miss_you: Path(IMAGES_DIR, 'miss-you.png'),
}
