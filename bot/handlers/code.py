import json

from telegram import Update
from telegram.ext import ContextTypes


async def web_app_data(update: Update, _: ContextTypes.DEFAULT_TYPE):
    data = json.loads(update.effective_message.web_app_data.data)
    print(data)
