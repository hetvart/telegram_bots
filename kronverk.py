from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode

from currency_api import CurrencyConverter


def exchange_rate(bot, update):
    chat_id = update.message.chat_id
    converter = CurrencyConverter()
    top_currencies_rates = [rate for rate in converter.get_exchange_rate() if
                            rate['cc'] in ('USD', 'EUR', 'GBP', 'RUB')]
    text = '\n'.join(['{currency_name} ({currency_code}): {currency_rate} грн'.format(currency_name=rate['txt'],
                                                                                      currency_code=rate['cc'],
                                                                                      currency_rate=str(rate['rate']))
                      for rate in top_currencies_rates])
    bot.send_message(chat_id=chat_id, text=text)


def convert(bot, update):
    chat_id = update.message.chat_id
    converter = CurrencyConverter()
    text = str(converter.convert()) + ' грн'
    bot.send_message(chat_id=chat_id, text=text)


def help(bot, update):
    chat_id = update.message.chat_id
    text = 'Привіт! Мене звати Кронверк. Я простий бот, який дозволяє швидко дізнатись курс валют на поточну дату. ' \
           'Якщо бажаєш дізнатись актуальний курс валют, просто ' \
           'напиши /exchange\_rate.'
    # text = 'Привіт! Мене звати Кронверк. Я простий бот, який дозволяє швидко дізнатись курс валют на поточну дату ' \
    #        'або конвертувати валюту з однієї в іншу. ' \
    #        'Якщо бажаєш дізнатись актуальний курс валют, просто ' \
    #        'напиши /exchange\_rate. Щоб конвертувати валюту, напиши /convert'
    bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN)


def reply_to_message(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Я приймаю тільки команди, Карл!')


def reply_to_wrong_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Можливо, ти ввів якийсь лєвак. Топаз, повтори команду!')


def main():
    updater = Updater(token='681821774:AAHb_S7afR3BUOfHjwPqTlxAwY29kNoAxlE')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('exchange_rate', exchange_rate))
    # dp.add_handler(CommandHandler('convert', convert))
    wrong_command_handler = MessageHandler(Filters.command, reply_to_wrong_command)
    message_handler = MessageHandler(Filters.text, reply_to_message)
    dp.add_handler(message_handler)
    dp.add_handler(wrong_command_handler)
    updater.start_polling()
    updater.idle()


main()
