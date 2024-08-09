import logging
import os
from random import choice

from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    Updater,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update

from apis import CurrencyConverter, OpenWeatherApi
from vars import PREDICTIONS, SHIT

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.ERROR
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    weather_btn = KeyboardButton(text="Погода", request_location=True)
    exchange_rate_btn = KeyboardButton(text="Курс валют")
    fortune_cookie_btn = KeyboardButton(text="Передбачення")
    menu = [[weather_btn, exchange_rate_btn, fortune_cookie_btn]]
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Йоу, я Кронверк! Чим я можу тобі допомогти?",
        reply_markup=reply_markup,
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{update.message.text}? {choice(SHIT)}",
    )


async def currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    converter = CurrencyConverter()
    rate = converter.get_base_exchange_rate()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=rate)


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    weather_api = OpenWeatherApi()
    weather = weather_api.get_current_weather_data(
        lat=location["latitude"], lon=location["longitude"]
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=weather)


async def fortune_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prediction = choice(PREDICTIONS)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=prediction)


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("KRONVERK_API_TOKEN")).build()

    # Start command handler
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    # Location handler
    location_handler = MessageHandler(filters.LOCATION, location)
    application.add_handler(location_handler)

    # Fortune handler
    fortune_handler = MessageHandler(
        filters.TEXT & filters.Regex("^Передбачення$"), fortune_handler
    )
    application.add_handler(fortune_handler)

    # Currency rate handler
    currency_handler = MessageHandler(
        filters.TEXT & filters.Regex("^Курс валют$"), currency
    )
    application.add_handler(currency_handler)

    # Echo handler
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    application.run_polling()
