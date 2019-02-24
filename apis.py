import os
import requests


class CurrencyConverter(object):
    api_url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'

    def get_exchange_rate(self):
        return requests.get(self.api_url).json()


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
