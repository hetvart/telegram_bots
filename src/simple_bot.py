from http import HTTPStatus
from typing import AsyncGenerator
from contextlib import asynccontextmanager
import os
import logging
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import Application
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Initialize Telegram Application
application = Application.builder().token(os.getenv("BOT_TOKEN")).build()


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


# Define command and message handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello! I'm your bot."
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


@app.post("/webhook")
async def process_update(request: Request):
    if not application.running:
        await application.initialize()
    req = await request.json()
    update = Update.de_json(req, application.bot)
    await application.process_update(update)
    return Response(status_code=HTTPStatus.OK)


# Health check bot is up and running
@app.get("/")
async def index():
    return {"message": "Bot is running"}
