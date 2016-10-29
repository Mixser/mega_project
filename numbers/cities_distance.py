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


def get_distance(first, second):
    radius = 6371e3

    phi1, phi2 = first[0] * math.pi / 180.0, second[0] * math.pi / 180.0

    d_lat, d_lng = (second[0] - first[0]) * math.pi / 180.0, (second[1] - first[1]) * math.pi / 180.0

    a = math.sin(d_lat / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lng / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return radius * c


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "You must provide two cities as program's arguments"

    first_city = sys.argv[1]
    second_city = sys.argv[2]

    first_city_location = get_city_location(first_city)
    second_city_location = get_city_location(second_city)

    distance = get_distance(first_city_location, second_city_location) / 1000.0

    output_str = "Distance between {0} and {1} is {2:.2f} km.".format(first_city,
                                                                  second_city,
                                                                  distance)

    print output_str
