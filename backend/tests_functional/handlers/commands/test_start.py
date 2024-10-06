
import asyncpg
from pytest_mock import MockerFixture
from telegram import InlineKeyboardButton, WebAppInfo
from telegram import User as TGUser

from src.bot.handlers.commands import start_handler
from tests_functional.utils import add_user


async def test_start_handler__new_user__link_lead_to_choose_level(
    pg: asyncpg.Pool,
    mocker: MockerFixture,
) -> None:
    # arrange
    telegram_id = 1
    update_mock = mocker.AsyncMock()
    update_mock.message = mocker.AsyncMock()
    update_mock.message.text = ''
    update_mock.message.from_user = TGUser(id=telegram_id, is_bot=False, first_name='first_name')

    await mocker.patch('src.bot.handlers.commands.pg_pool', pg)

    mocker.patch('src.bot.handlers.commands.bot_settings.WEB_APP_URL', 'https://web-app-url.com')

    # act
    await start_handler(update_mock, None)

    # assert
    # send message
    assert update_mock.message.reply_photo.call_count == 1
    assert update_mock.message.reply_photo.call_args.kwargs['reply_markup']['inline_keyboard'] == (
        (
            InlineKeyboardButton(
                text='Играть в 1 клик! 🚀',
                web_app=WebAppInfo(url='https://web-app-url.com/choose-level')
            ),
        ),
    )


async def test_start_handler__user_already_created__link_lead_to_solve_questions(
    pg: asyncpg.Pool,
    mocker: MockerFixture,
) -> None:
    # arrange
    telegram_id = 1
    await add_user(pg=pg, telegram_id=telegram_id)
    update_mock = mocker.AsyncMock()
    update_mock.message = mocker.AsyncMock()
    update_mock.message.text = ''
    update_mock.message.from_user = TGUser(id=telegram_id, is_bot=False, first_name='first_name')

    await mocker.patch('src.bot.handlers.commands.pg_pool', pg)

    mocker.patch('src.bot.handlers.commands.bot_settings.WEB_APP_URL', 'https://web-app-url.com')

    # act
    await start_handler(update_mock, None)

    # assert
    # send message
    assert update_mock.message.reply_photo.call_count == 1
    assert update_mock.message.reply_photo.call_args.kwargs['reply_markup']['inline_keyboard'] == (
        (
            InlineKeyboardButton(
                text='Изменить уровень 🎓',
                web_app=WebAppInfo(url='https://web-app-url.com/choose-level')),
        ),
        (
            InlineKeyboardButton(
                text='Играть в 1 клик! 🚀',
                web_app=WebAppInfo(url='https://web-app-url.com/solve-question')),
        )
    )
