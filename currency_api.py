import requests


class CurrencyConverter(object):
    api_url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'

    def get_exchange_rate(self):
        return requests.get(self.api_url).json()

    def convert(self, _from='USD', to='UAH', amount=1):
        exchange_rate = self.get_exchange_rate()
        rate = [currency['rate'] for currency in exchange_rate if currency['cc'] == _from.upper()][0]
        rate = rate * amount
        return round(rate, 4)
