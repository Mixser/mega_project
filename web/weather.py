# -*- coding: utf-8 -*-

import requests

import argparse

APPID = '9a3675b6715bf378ff635db295ea7a2d' # place your APPID from openweathermap.org

day = {
    u'01d': u'\u2600\ufe0f',
    u'02d': u'\U0001f324',
    u'03d': u'\U0001f325',
    u'04d': u'\U0001f325',
    u'09d': u'\U0001f326',
    u'10d': u'\U0001f326',
    u'11d': u'\u26c8',
    u'13d': u'\u2744\ufe0f',
    u'01n': u'\u2600\ufe0f',
    u'02n': u'\U0001f324',
    u'03n': u'\U0001f325',
    u'04n': u'\U0001f325',
    u'09n': u'\U0001f326',
    u'10n': u'\U0001f326',
    u'11n': u'\u26c8',
    u'13n': u'\u2744\ufe0f'
}


class Weather(object):

    def __init__(self, api_response):
        data = dict(api_response['main'])
        data.update(api_response['weather'][0])

        self.main = None
        self.icon = None
        self.description = None
        self.temp_max = None
        self.temp_min = None
        self.temp = None
        self.humidity = None
        self.city = None
        self.country = None

        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.city = api_response['name']
        self.country = api_response['sys']['country']
        self.icon = day.get(self.icon, self.icon)

    def __unicode__(self):
        first_line = u"Weather at {city}, {country}"
        second_line = u"Temp: {temp}, Min: {temp_min}, Max: {temp_max}"
        third_line = u"{main}, {description}, {icon}"
        fourth_line = u"Humidity: {humidity}%"

        final = u'\n'.join((first_line, second_line, third_line, fourth_line))
        return final.format(**self.__dict__)

    def __str__(self):
        return unicode(self).encode('utf-8')


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


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--city', help='Get weather for a specific city.', default='')
    parser.add_argument('--country', default='')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse()
    if not args.city:
        ip_address = get_external_ip()
        country, city = get_location_by_id(ip_address)
    else:
        country, city = args.country, args.city

    w = get_weather(city, country)

    print w

