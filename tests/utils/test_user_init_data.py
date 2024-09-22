from pytest_mock import MockerFixture

from src.models.users import TelegramUser, UserInitData
from src.utils.user_init_data import validate_and_parce_user_init_data


def test_validate_and_parce_user_init_data(mocker: MockerFixture) -> None:
    # arrange
    user_id = 1
    first_name = 'John'
    language_code = 'en'
    user_hash = '4f97fa2703d6a8088bcb68eb038c7308fd5c1b6ce30874c389b03ce53f850795'
    user_init_data_raw = (
        f'user=%7B%22id%22%3A{user_id}%2C%22first_name%22%3A%22{first_name}'
        f'%22%2C%22language_code%22%3A%22{language_code}%22%7D&hash={user_hash}'
    )

    mocker.patch('src.utils.user_init_data.bot_settings.TOKEN', 'token')

    # act
    user_init_data = validate_and_parce_user_init_data(user_init_data_raw)

    # assert
    assert user_init_data == UserInitData(
        hash=user_hash,
        user=TelegramUser(id=user_id, first_name=first_name, language_code=language_code)
    )


def test_validate_and_parce_user_init_data__no_hash() -> None:
    # arrange
    user_id = 1
    first_name = 'John'
    language_code = 'en'
    user_init_data_raw = (
        f'user=%7B%22id%22%3A{user_id}%2C%22first_name%22%3A%22{first_name}'
        f'%22%2C%22language_code%22%3A%22{language_code}%22%7D'
    )

    # act
    user_init_data = validate_and_parce_user_init_data(user_init_data_raw)

    # assert
    assert user_init_data is None


def test_validate_and_parce_user_init_data__no_user() -> None:
    # arrange
    user_hash = '123'
    user_init_data_raw = f'hash={user_hash}'

    # act
    user_init_data = validate_and_parce_user_init_data(user_init_data_raw)

    # assert
    assert user_init_data is None


def test_validate_user_init_data__invalid_hash(mocker: MockerFixture) -> None:
    # arrange
    user_id = 1
    first_name = 'John'
    language_code = 'en'
    user_hash = '123'
    user_init_data_raw = (
        f'user=%7B%22id%22%3A{user_id}%2C%22first_name%22%3A%22{first_name}'
        f'%22%2C%22language_code%22%3A%22{language_code}%22%7D&hash={user_hash}'
    )

    mocker.patch('src.utils.user_init_data.bot_settings.TOKEN', 'token')

    # act
    user_init_data = validate_and_parce_user_init_data(user_init_data_raw)

    # assert
    assert user_init_data is None
