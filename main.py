from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import os
from dotenv import load_dotenv
from scrape_stock_price import getStockPrice

load_dotenv()

TOKEN: Final = os.getenv("API_TOKEN")
BOT_USERNAME: Final = os.getenv("API_USERNAME")

INPUT_STATE = 0

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! Use /track to set tracking for stock.")
# ** Add track command

async def track_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send name of stock you would like me to track.")
    # user_text = update.message.text
    # print("track command user: ", user_text)
    return INPUT_STATE

    # await update.message.reply_text("The default frequency of sending update of price is 1 hour, want to change it? Use /frequency")

# ** Add remove track command
# ** Add update frequency command
# ** Add send price message from Bot command

async def cancel_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Something wrong happened....")
    return ConversationHandler.END


async def handle_input(update, context):
    userInput = update.message.text
    print("handle input: ", userInput)

    value = getStockPrice(userInput)
    if value is None:
        await update.message.reply_text("Sorry, could not find what you are looking for. Try /track again.")
        return ConversationHandler.END
    await update.message.reply_text(userInput + ": $" + value)
    return ConversationHandler.END

if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('track', track_command)],
        states={
            INPUT_STATE: [MessageHandler(filters.TEXT, handle_input), ]
        },
        fallbacks=[CommandHandler('cancel', cancel_command)]
    )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('start', start_command))

    print("Polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
    