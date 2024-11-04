from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN: Final = os.getenv("API_TOKEN")
BOT_USERNAME: Final = os.getenv("API_USERNAME")

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! Use /track <stock> to set tracking for price on that stock.")


if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))

    print("Polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
    