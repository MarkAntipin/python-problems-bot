import typing as tp

import asyncpg
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from tests_functional.utils import add_user


async def test_send_payment__ok(
    client: TestClient,
    pg: asyncpg.Pool,
    user_init_data: tp.Callable[..., str],
    mocker: MockerFixture
) -> None:
    # arrange
    tg_user_id: int = 1
    user_level: int = 1
    await add_user(pg=pg, level=user_level, telegram_id=tg_user_id)
    user_init_data_raw = user_init_data(user_id=tg_user_id)
    send_payment_mock = mocker.patch('src.api.routers.v1.payment.send_payment')

    # act
    resp = client.post(
        '/api/v1/payment/send-payment',
        json={
            'user_init_data': user_init_data_raw
        },
    )

    # assert
    assert resp.status_code == status.HTTP_200_OK
    assert send_payment_mock.call_count == 1
