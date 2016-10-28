import requests
import math

import sys

url = 'http://maps.googleapis.com/maps/api/geocode/json'


def get_city_location(city_name):
    r = requests.get(url, params={'sensor': 'false', 'address': city_name})

    data = r.json()

    if not r.ok or data['status'] != 'OK':
        raise AttributeError("We can't find the city with name %s" % city_name)

    lat = float(data['results'][0]['geometry']['location']['lat'])
    lng = float(data['results'][0]['geometry']['location']['lng'])

    return lat, lng


def distance(first, second):
    radius = 6371e3

    phi1, phi2 = first[0] * math.pi / 180.0, second[0] * math.pi / 180.0

    d_lat, d_lng = (second[0] - first[0]) * math.pi / 180.0, (second[1] - first[1]) * math.pi / 180.0

    a = math.sin(d_lat / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lng / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return radius * c


if __name__ == '__main__':

    f_lat, f_lng = get_city_location(sys.argv[1])
    s_lat, s_lng = get_city_location(sys.argv[2])

    print 'Distance:', distance((f_lat, f_lng), (s_lat, s_lng)) / 1000, "km."
