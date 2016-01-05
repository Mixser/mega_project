import requests

APPID = '' # place your APPID from openweathermap.org


class Weather(object):
    main = None
    icon = None
    description = None

    temp_max = None
    temp_min = None
    temp = None

    humidity = None

    city = None
    country = None

    def __init__(self, api_response):
        data = dict(api_response['main'])
        data.update(api_response['weather'][0])

        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.city = api_response['name']
        self.country = api_response['sys']['country']

    def __str__(self):
        first_line = "Weather at {city}, {country}"
        second_line = "Temp: {temp}, Min: {temp_min}, Max: {temp_max}"
        third_line = "{main}, {description}"
        last_line = "Humidity: {humidity}%"

        final = '\n'.join((first_line, second_line, third_line, last_line))

        return final.format(**self.__dict__)


def get_external_ip():
    r = requests.get('http://ip.42.pl/raw')
    ip_addr = r.content

    return ip_addr


def get_location_by_id(ip_address):
    url = 'http://ip-api.com/json/' + ip_address
    r = requests.get(url)

    data = r.json()

    return data['country'], data['city']


def get_weather(city, country):
    query_params = {
        'q': '{},{}'.format(city, country),
        'APPID': APPID,
        'units': 'metric'
    }

    url = 'http://api.openweathermap.org/data/2.5/weather'

    r = requests.get(url, query_params)

    return Weather(r.json())

if __name__ == '__main__':
    ip_address = get_external_ip()
    country, city = get_location_by_id(ip_address)

    w = get_weather(city, country)

    print w

