# -*- coding: utf-8 -*-

import requests

APPID = '' # place your APPID from openweathermap.org

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
        self.icon = day.get(self.icon, self.icon)

    def _get_data(self):
        keys = filter(lambda x: not x.startswith('_'), dir(self))

        return {key: getattr(self, key) for key in keys}

    def __unicode__(self):
        first_line = u"Weather at {city}, {country}"
        second_line = u"Temp: {temp}, Min: {temp_min}, Max: {temp_max}"
        third_line = u"{main}, {description}, {icon}"
        fourth_line = u"Humidity: {humidity}"

        final = u'\n'.join((first_line, second_line, third_line, fourth_line))
        return final.format(**self._get_data())

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

if __name__ == '__main__':
    ip_address = get_external_ip()
    country, city = get_location_by_id(ip_address)

    w = get_weather(city, country)

    print w

