import hashlib
import hmac
import logging
from urllib.parse import parse_qsl, unquote

from settings import bot_settings
from src.models.users import TelegramUser, UserInitData

logger = logging.getLogger(__name__)


def validate_and_parce_user_init_data(user_init_data_raw: str) -> UserInitData | None:
    """
    user init data validation;
    check: https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    """
    user_init_data = dict(parse_qsl(user_init_data_raw))

    if not user_init_data.get('hash'):
        logger.error('Invalid user_init_data: hash is required')
        return

    if not user_init_data.get('user'):
        logger.error('Invalid user_init_data: user is required')
        return

    received_hash = user_init_data['hash']
    fields = sorted(
        [(key, unquote(value)) for key, value in user_init_data.items() if key != 'hash']
    )
    data_check_string = '\n'.join(f'{k}={v}' for k, v in fields)
    secret_key = hmac.new(
        b'WebAppData', bot_settings.TOKEN.encode(), hashlib.sha256
    ).digest()
    computed_hash = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()
    if computed_hash != received_hash:
        logger.error('Invalid user_init_data: hash is invalid')
        return

    return UserInitData(
        user=TelegramUser.model_validate_json(unquote(user_init_data['user'])),
        hash=user_init_data['hash']
    )
