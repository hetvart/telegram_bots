import os
from random import choice

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup

from src.apis import CurrencyConverter, OpenWeatherApi
from src.vars import PREDICTIONS


def start(bot, update):
    weather_btn = KeyboardButton(text='Погода', request_location=True)
    exchange_rate_btn = KeyboardButton(text='Курс валют')
    fortune_cookie_btn = KeyboardButton(text='Передбачення')
    menu = [[weather_btn, exchange_rate_btn, fortune_cookie_btn]]
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text='Йоу, я Кронверк! Чим я можу тобі допомогти?',
                     reply_markup=reply_markup)


def reply_to_location(bot, update):
    location = update.message.location
    weather_api = OpenWeatherApi()
    weather = weather_api.get_current_weather_data(lat=location['latitude'], lon=location['longitude'])
    bot.send_message(chat_id=update.message.chat_id, text=weather)


def reply_to_message(bot, update):
    text = 'Можливо, ти ввів якийсь лєвак. Топаз, повтори команду!'
    if update.message.text == 'Курс валют':
        converter = CurrencyConverter()
        text = converter.get_base_exchange_rate()
    if update.message.text == 'Передбачення':
        text = choice(PREDICTIONS)
    bot.send_message(chat_id=update.message.chat_id, text=text)


def reply_to_wrong_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Можливо, ти ввів якийсь лєвак. Топаз, повтори команду!')


def main():
    telegram_api_bot_token = os.environ.get('TELEGRAM_API_BOT_TOKEN')
    updater = Updater(token=telegram_api_bot_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    wrong_command_handler = MessageHandler(Filters.command, reply_to_wrong_command)
    message_handler = MessageHandler(Filters.text, reply_to_message)
    location_handler = MessageHandler(Filters.location, reply_to_location)
    dp.add_handler(message_handler)
    dp.add_handler(wrong_command_handler)
    dp.add_handler(location_handler)
    updater.start_polling()
    updater.idle()


main()
