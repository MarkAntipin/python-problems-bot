from datetime import UTC, datetime, timedelta
from logging import getLogger

from pydantic import BaseModel

from src.services.models.payment_status import PaymentStatus
from src.services.users import User

# THREE_DAYS = timedelta(days=3)
THREE_DAYS = timedelta(minutes=1)

logger = getLogger(__name__)


class PaymentInfo(BaseModel):
    is_need_to_send_payment: bool
    is_passed_paywall: bool


def get_payment_info(user: User) -> PaymentInfo:
    match user.payment_status:
        case PaymentStatus.onboarding:
            return PaymentInfo(
                is_need_to_send_payment=False,
                is_passed_paywall=False
            )

        case PaymentStatus.paid:
            return PaymentInfo(
                is_need_to_send_payment=False,
                is_passed_paywall=True
            )

        case PaymentStatus.trial:
            if not user.start_trial_at:
                logger.error('User %d has no start_trial_at', user.id)
                return PaymentInfo(
                    is_need_to_send_payment=True,
                    is_passed_paywall=False
                )

            now = datetime.now(UTC)
            if now - user.start_trial_at > THREE_DAYS:
                return PaymentInfo(
                    is_need_to_send_payment=not bool(user.send_payment_at),
                    is_passed_paywall=False
                )
            else:
                return PaymentInfo(
                    is_need_to_send_payment=False,
                    is_passed_paywall=True
                )
        case _:
            logger.error('User %d has unknown payment status', user.id)
