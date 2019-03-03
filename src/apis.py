import os
from operator import itemgetter

import requests

from src.tools import flag


class CurrencyConverter(object):
    api_url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'

    def get_exchange_rate(self):
        return requests.get(self.api_url).json()

    @staticmethod
    def get_base_exchange_rate():
        """
        :return: Preformatted base currencies rates: US dollar, Euro, UK Pound, Russian ruble
        """
        converter = CurrencyConverter()
        top_currencies_rates = [rate for rate in converter.get_exchange_rate() if
                                rate['cc'] in ('USD', 'EUR', 'GBP', 'RUB')]
        top_currencies_rates = sorted(top_currencies_rates, key=itemgetter('rate'), reverse=True)
        countries_flags = iter([flag(code) for code in ('gb', 'eu', 'us', 'ru')])
        text = '\n'.join(
            ['{flag} {currency_name} ({currency_code}): {currency_rate} грн'.format(currency_name=rate['txt'],
                                                                                    currency_code=rate['cc'],
                                                                                    currency_rate=str(
                                                                                        rate['rate']),
                                                                                    flag=next(countries_flags))
             for rate in top_currencies_rates])

        return text


class OpenWeatherApi(object):
    api_url = 'http://api.openweathermap.org/data/2.5/weather'
    token = os.environ.get('OPEN_WEATHER_API_TOKEN')

    def get_current_weather_data(self, lat=50.43, lon=30.52):
        """
        :param lat: latitude
        :param lon: longitude
        :return: Actual temp for the given location,  e.g. Kiev: -1 °C
        """
        query = '?lat={lat}&lon={lon}&units=metric&APPID={token}'.format(lat=lat, lon=lon, token=self.token)
        request_url = self.api_url + query
        response = requests.get(url=request_url).json()
        return "{}: {} \N{DEGREE SIGN}C".format(response['name'], round(response['main']['temp']))
