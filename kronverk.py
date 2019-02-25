import os
from operator import itemgetter
from random import choice

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode

from apis import CurrencyConverter, OpenWeatherApi
from tools import flag
from vars import PREDICTIONS


def exchange_rate(bot, update):
    chat_id = update.message.chat_id
    converter = CurrencyConverter()
    top_currencies_rates = [rate for rate in converter.get_exchange_rate() if
                            rate['cc'] in ('USD', 'EUR', 'GBP', 'RUB')]
    top_currencies_rates = sorted(top_currencies_rates, key=itemgetter('rate'), reverse=True)
    countries_flags = iter([flag(code) for code in ('gb', 'eu', 'us', 'ru')])
    text = '\n'.join(['{flag} {currency_name} ({currency_code}): {currency_rate} грн'.format(currency_name=rate['txt'],
                                                                                             currency_code=rate['cc'],
                                                                                             currency_rate=str(
                                                                                                 rate['rate']),
                                                                                             flag=next(countries_flags))
                      for rate in top_currencies_rates])

    bot.send_message(chat_id=chat_id, text=text)


def start(bot, update):
    chat_id = update.message.chat_id
    text = 'Привіт! Мене звати Кронверк. Я простий бот, який вміє робити різні цікаві штуки.' \
           'Якщо бажаєш дізнатись актуальний курс валют, просто ' \
           'напиши /exchange\_rate. Щоб дізнатись погоду, просто відправ мені своє розташування.'
    bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN)


def fortune_cookie(bot, update):
    chat_id = update.message.chat_id
    text = choice(PREDICTIONS)
    bot.send_message(chat_id=chat_id, text=text)


def reply_to_location(bot, update):
    location = update.message.location
    weather_api = OpenWeatherApi()
    weather = weather_api.get_current_weather_data(lat=location['latitude'], lon=location['longitude'])
    bot.send_message(chat_id=update.message.chat_id, text=weather)


def reply_to_message(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Я приймаю тільки команди, Карл!')


def reply_to_wrong_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Можливо, ти ввів якийсь лєвак. Топаз, повтори команду!')


def main():
    telegram_api_bot_token = os.environ.get('TELEGRAM_API_BOT_TOKEN')
    updater = Updater(token=telegram_api_bot_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('exchange_rate', exchange_rate))
    dp.add_handler(CommandHandler('fortune_cookie', fortune_cookie))
    wrong_command_handler = MessageHandler(Filters.command, reply_to_wrong_command)
    message_handler = MessageHandler(Filters.text, reply_to_message)
    location_handler = MessageHandler(Filters.location, reply_to_location)
    dp.add_handler(message_handler)
    dp.add_handler(wrong_command_handler)
    dp.add_handler(location_handler)
    updater.start_polling()
    updater.idle()


main()
