from datetime import UTC, datetime, timedelta

import pytest

from src.models.payment_status import PaymentStatus
from src.services.users import User
from src.utils.payment import PaymentInfo, get_payment_info


@pytest.mark.parametrize(
    'user, expected',
    [
        (
            User(
                id=1,
                telegram_id=1,
                payment_status=PaymentStatus.onboarding,
                level=1,
                status='active'
            ),
            PaymentInfo(is_need_to_send_payment=False, is_passed_paywall=True)
        ),
        (
            User(
                id=1,
                telegram_id=1,
                payment_status=PaymentStatus.trial,
                level=1,
                status='active',
                start_trial_at=None
            ),
            PaymentInfo(is_need_to_send_payment=True, is_passed_paywall=False)
        ),
        (
            User(
                id=1,
                telegram_id=1,
                payment_status=PaymentStatus.trial,
                level=1,
                status='active',
                start_trial_at=datetime.now(UTC) - timedelta(days=4)
            ),
            PaymentInfo(is_need_to_send_payment=True, is_passed_paywall=False)
        ),
        (
            User(
                id=1,
                telegram_id=1,
                payment_status=PaymentStatus.trial,
                level=1,
                status='active',
                start_trial_at=datetime.now(UTC) - timedelta(days=2)
            ),
            PaymentInfo(is_need_to_send_payment=False, is_passed_paywall=True)
        ),
        (
            User(
                id=1,
                telegram_id=1,
                payment_status=PaymentStatus.paid,
                level=1,
                status='active',
            ),
            PaymentInfo(is_need_to_send_payment=False, is_passed_paywall=True)
        ),
        (
            User(
                id=1,
                telegram_id=1,
                payment_status=PaymentStatus.trial,
                level=1,
                status='active',
                send_payment_at=datetime.now(UTC),
                start_trial_at=datetime.now(UTC) - timedelta(days=4)
            ),
            PaymentInfo(is_need_to_send_payment=False, is_passed_paywall=False)
        ),
    ]
)
def test_get_payment_info(user: User, expected: bool) -> None:
    # act
    res = get_payment_info(user=user)

    # assert
    assert res == expected
