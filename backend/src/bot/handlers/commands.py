import logging

from telegram import Update
from telegram import User as TGUser
from telegram.ext import ContextTypes

from settings import bot_settings
from src.images import ImageType
from src.mappers.users import map_inner_telegram_user_from_tg_user
from src.services.achievements import AchievementsService
from src.services.leaders import LeadersService
from src.services.users import UsersService
from src.texts import CHANGE_LEVEL_BUTTON_TEXT, GREETING_TEXT, START_BUTTON_TEXT
from src.utils.formaters import format_achievements_list, format_leaders_message
from src.utils.postgres_pool import pg_pool
from src.utils.telegram.inline_keyboard import KeyboardButtonForFormatting
from src.utils.telegram.send_message import send_message

logger = logging.getLogger(__name__)


def _get_deep_link_param(update: Update) -> str | None:
    if not update.message:
        return

    if not update.message.text:
        return

    parts = update.message.text.split('/start ')
    if len(parts) >= 2:
        return parts[1]


async def start_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    came_from: str | None = _get_deep_link_param(update=update)

    users_service = UsersService(pg_pool=pg_pool)
    tg_user: TGUser = update.message.from_user
    user, is_created = await users_service.get_or_create(
        tg_user=map_inner_telegram_user_from_tg_user(tg_user), came_from=came_from
    )

    # if user block bot and then start again
    await users_service.set_status(user_id=user.id, status='active')
    logger.info('User %d run start handler', user.id)

    keyboard_buttons = [
        KeyboardButtonForFormatting(
            text=START_BUTTON_TEXT,
            web_app_url=f'{bot_settings.WEB_APP_URL}/choose-level'
        ),
    ]

    # if it is an old user, he can change level
    if not is_created:
        keyboard_buttons.insert(
            0,
            KeyboardButtonForFormatting(
                text=CHANGE_LEVEL_BUTTON_TEXT,
                web_app_url=f'{bot_settings.WEB_APP_URL}/choose-level'
            )
        )

    await send_message(
        message=update.message,
        text=GREETING_TEXT,
        keyboard_buttons=keyboard_buttons,
        image=ImageType.greeting
    )


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass


async def leaders_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    leaders_service = LeadersService(pg_pool=pg_pool)
    users_service = UsersService(pg_pool=pg_pool)

    tg_user: TGUser = update.message.from_user
    user, _ = await users_service.get_or_create(tg_user=map_inner_telegram_user_from_tg_user(tg_user))
    logger.info('User %d run leaders handler', user.id)

    leaders = await leaders_service.get_top_users(limit=5)
    if not leaders:
        # TODO: add logging
        return

    user_in_leaders = await leaders_service.get_user_in_leaders(user_id=user.id)

    message_text = format_leaders_message(
        leaders=leaders,
        user_in_leaders=user_in_leaders
    )

    await send_message(message=update.message, text=message_text)
    # TODO: кнопка назад


async def get_achievements_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    users_service = UsersService(pg_pool=pg_pool)
    achievements_service = AchievementsService(pg_pool=pg_pool)

    tg_user: TGUser = update.message.from_user
    user, _ = await users_service.get_or_create(tg_user=map_inner_telegram_user_from_tg_user(tg_user))
    logger.info('User %d run achievements handler', user.id)

    achievements = await achievements_service.get_user_achievements(user_id=user.id)
    await send_message(
        message=update.message, text=format_achievements_list(achievements=achievements)
    )
    # TODO: кнопка назад

