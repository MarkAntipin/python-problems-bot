from datetime import UTC, datetime, timedelta

import pytest

from src.services.models.payment_status import PaymentStatus
from src.services.users import User
from src.utils.paywall import is_need_to_send_payment, is_passed_paywall


@pytest.mark.parametrize(
    'user,is_passed',
    [
        (
            User(
                id=1,
                telegram_id=1,
                level=1,
                payment_status=PaymentStatus.onboarding,
            ),
            False
        ),
        (
            User(
                id=1,
                telegram_id=1,
                level=1,
                payment_status=PaymentStatus.trial,
                start_trial_at=datetime.now(UTC) - timedelta(days=2),
            ),
            True
        ),
        (
            User(
                id=1,
                telegram_id=1,
                level=1,
                payment_status=PaymentStatus.trial,
                start_trial_at=datetime.now(UTC) - timedelta(days=4),
            ),
            False
        ),
        (
            User(
                id=1,
                telegram_id=1,
                level=1,
                payment_status=PaymentStatus.paid,
                last_paid_at=datetime.now(UTC) - timedelta(days=15),
            ),
            True
        ),
        (
            User(
                id=1,
                telegram_id=1,
                level=1,
                payment_status=PaymentStatus.paid,
                last_paid_at=datetime.now(UTC) - timedelta(days=32),
            ),
            False
        ),
    ]
)
def test_is_passed_paywall(user: User, is_passed: bool) -> None:
    res = is_passed_paywall(user=user)
    assert res == is_passed


@pytest.mark.parametrize(
    'user,is_need',
    [
        (
            User(
                id=1,
                telegram_id=1,
                level=1,
                payment_status=PaymentStatus.onboarding,
            ),
            False
        ),
        (
            User(
                id=1,
                telegram_id=1,
                level=1,
                payment_status=PaymentStatus.trial,
            ),
            True
        ),
        (
            User(
                id=1,
                telegram_id=1,
                level=1,
                payment_status=PaymentStatus.trial,
                send_payment_at=datetime.now(UTC),
            ),
            False
        ),
        (
            User(
                id=1,
                telegram_id=1,
                level=1,
                payment_status=PaymentStatus.paid,
                last_paid_at=datetime.now(UTC) - timedelta(days=15),
            ),
            False
        ),
        (
            User(
                id=1,
                telegram_id=1,
                level=1,
                payment_status=PaymentStatus.paid,
                last_paid_at=datetime.now(UTC) - timedelta(days=31),
            ),
            True
        ),
    ]
)
def test_is_need_to_send_payment(user: User, is_need: bool) -> None:
    res = is_need_to_send_payment(user=user)
    assert res == is_need
