import os
import requests

from operator import itemgetter
from src.tools import flag


class CurrencyConverter(object):
    api_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

    def get_exchange_rate(self):
        return requests.get(self.api_url).json()

    @staticmethod
    def get_base_exchange_rate():
        """
        :return: Preformatted base currencies rates: US dollar, Euro, UK Pound, Russian ruble
        """
        converter = CurrencyConverter()
        top_currencies_rates = [
            rate
            for rate in converter.get_exchange_rate()
            if rate["cc"] in ("USD", "EUR", "GBP")
        ]
        top_currencies_rates = sorted(
            top_currencies_rates, key=itemgetter("rate"), reverse=True
        )
        countries_flags = iter([flag(code) for code in ("gb", "eu", "us")])
        text = "\n".join(
            [
                "{flag} {currency_name} ({currency_code}): {currency_rate} грн".format(
                    currency_name=rate["txt"],
                    currency_code=rate["cc"],
                    currency_rate=str(rate["rate"]),
                    flag=next(countries_flags),
                )
                for rate in top_currencies_rates
            ]
        )

        return text


class OpenWeatherApi(object):
    api_url = "http://api.openweathermap.org/data/2.5/weather"
    token = os.environ.get("OPEN_WEATHER_API_KEY")

    def get_current_weather_data(self, lat: float, lon: float):
        """
        :param lat (float): latitude
        :param lon (float): longitude
        :return: Actual temp for the given location,  e.g. Kyiv: -1 °C
        """
        request_params = {
            "lat": lat,
            "lon": lon,
            "units": "metric",
            "appid": self.token,
        }
        response = requests.get(url=self.api_url, params=request_params)
        response.raise_for_status()
        response_body = response.json()

        return f"{response_body['name']}: {round(response_body['main']['temp'])} \N{DEGREE SIGN}C"
