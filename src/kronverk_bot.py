from contextlib import asynccontextmanager
from http import HTTPStatus
import logging
import os
from random import choice
from typing import AsyncGenerator

from fastapi import FastAPI, Request, Response
from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update

from src.apis import CurrencyConverter, OpenWeatherApi
from src.vars import PREDICTIONS, SHIT

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Initialize Telegram Application
application = Application.builder().token(os.getenv("KRONVERK_API_TOKEN")).build()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    await application.bot.setWebhook(
        "https://telegram-bots-kappa.vercel.app/webhook",
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )
    async with application:
        await application.initialize()
        yield
        await application.shutdown()


# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)


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
    await context.bot.send_message(chat_id=update.effective_chat.id, text=choice(SHIT))


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


@app.post("/webhook")
async def process_update(request: Request):
    if not application.running:
        await application.initialize()
    req = await request.json()
    update = Update.de_json(req, application.bot)
    await application.process_update(update)
    return Response(status_code=HTTPStatus.OK)


@app.get("/")
async def index():
    return {"message": "Bot is running"}
