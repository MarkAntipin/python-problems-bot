from enum import StrEnum, auto


class PaymentStatus(StrEnum):
    onboarding = auto()
    """have not started trial yet"""
    trial = auto()
    paid = auto()
