from telegram import Update

from src.bot.bot import create_bot


def main() -> None:
    bot = create_bot()
    bot.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
