from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, BasePersistence, JobQueue
import os
from dotenv import load_dotenv
from scrape_stock_price import getStockPrice

load_dotenv()

TOKEN: Final = os.getenv("API_TOKEN")
BOT_USERNAME: Final = os.getenv("API_USERNAME")

INPUT_STATE = 0

trackedList = []

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! Use /track to set tracking for stock.")

async def track_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send name of stock you would like me to track.")
    return INPUT_STATE

# ** Add remove track command
# ** Add update frequency command
# ** Add send price message from Bot command

async def cancel_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Something wrong happened....")
    return ConversationHandler.END

async def stop_alert_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    context.bot_data['run_alerts'] = False
    print("STOP ALERTS: ", context.bot_data['run_alerts'])
    await update.message.reply_text("Stopping ALERTS...")


async def alert_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    context.bot_data['run_alerts'] = True
    await update.message.reply_text("Starting alerts, sending every minute...")
    chat_id = update.effective_message.chat_id
    job = context.job_queue.run_repeating(send_alert, interval=3600, chat_id=chat_id)
    await job.run(context.application)
    print("END OF ALERT COMMAND:")
    
    await update.message.reply_text("To end alerts, use /stop...")


async def send_alert(context:ContextTypes.DEFAULT_TYPE):
    job = context.job
    if context.bot_data['run_alerts'] == False:
        return
    print("START OF SEND ALERT:")
    for stock in trackedList:
        print("Name of stock: ", stock)
        value = getStockPrice(stock)
        message = stock + ": $" + value
        await context.bot.send_message(job.chat_id, text=message)

async def handle_input(update, context):
    userInput = update.message.text
    print("handle input: ", userInput)

    value = getStockPrice(userInput)
    if value is None:
        await update.message.reply_text("Sorry, could not find what you are looking for. Try /track again.")
        return ConversationHandler.END
    if userInput not in trackedList:
        trackedList.append(userInput)
    # await update.message.reply_text(userInput + ": $" + value)
    await update.message.reply_text("Adding to your tracked list for alerts, use /alert to start getting updates")
    return ConversationHandler.END

async def handle_response(update, context):
    await update.message.reply_text('Busy looking at stocks, try using commands...')

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
    app.add_handler(CommandHandler('alert', alert_command))
    app.add_handler(CommandHandler('stop', stop_alert_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_response))
    app.bot_data['run_alerts'] = True
    print("Polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)    