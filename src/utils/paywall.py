from datetime import UTC, datetime

from settings import THIRTY_DAYS, THREE_DAYS
from src.services.models.payment_status import PaymentStatus
from src.services.users import User


def is_passed_paywall(user: User) -> bool:
    now = datetime.now(UTC)

    if user.payment_status == PaymentStatus.onboarding:
        return False

    if user.payment_status == PaymentStatus.trial:
        if not user.start_trial_at:
            return False

        if now - user.start_trial_at < THREE_DAYS:
            return True

    if user.payment_status == PaymentStatus.paid:
        if not user.last_paid_at:
            return False

        if now - user.last_paid_at < THIRTY_DAYS:
            return True

    return False
