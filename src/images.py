from enum import StrEnum, auto
from pathlib import Path

from settings import IMAGES_DIR


class ImageType(StrEnum):
    greeting = auto()
    onboarding_finish = auto()
    onboarding_start = auto()


IMAGE_TYPE_TO_IMAGE_PATH = {
    ImageType.greeting: Path(IMAGES_DIR, 'greeting.png'),
    ImageType.onboarding_finish: Path(IMAGES_DIR, 'onboarding_finish.png'),
    ImageType.onboarding_start: Path(IMAGES_DIR, 'onboarding_start.png'),
}
