import requests


class CurrencyConverter(object):
    api_url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'

    def get_exchange_rate(self):
        return requests.get(self.api_url).json()


class OpenWeatherApi(object):
    api_url = 'http://api.openweathermap.org/data/2.5/weather'
    token = '6db04ae35b9e23276902b7b6bb48119a'

    def get_current_weather_data_by_coordinations(self, lat=50.43, lon=30.52):
        query = '?lat={lat}&lon={lon}&units=metric&APPID={token}'.format(lat=lat, lon=lon, token=self.token)
        request_url = self.api_url + query
        response = requests.get(url=request_url).json()
        return "{}: {} \N{DEGREE SIGN}C".format(response['name'], round(response['main']['temp']))
