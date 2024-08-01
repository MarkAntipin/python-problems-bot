from enum import StrEnum, auto


class States(StrEnum):
    daily_question = auto()
    onboarding = auto()
    change_level = auto()
    finish_onboarding = auto()
    code = auto()
