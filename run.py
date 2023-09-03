from telegram import Update

from bot.bot import create_bot
from settings import bot_settings


def main() -> None:
    bot = create_bot(bot_settings=bot_settings)
    bot.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
