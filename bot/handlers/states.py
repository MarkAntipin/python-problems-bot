from enum import StrEnum, auto


class States(StrEnum):
    daily_question = auto()
    onboarding = auto()
    finish_onboarding = auto()
