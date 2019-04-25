import requests
import math


def get_geo_info(city_name, type_info):
    if type_info == 'coordinates':
        try:
            url = "https://geocode-maps.yandex.ru/1.x/"
            params = {
                'geocode': city_name,
                'format': 'json'
            }
            response = requests.get(url, params)
            json = response.json()
            coordinates_str = json['response']['GeoObjectCollection'][
                'featureMember'][0]['GeoObject']['Point']['pos']
            long, lat = map(float, coordinates_str.split())
            return long, lat
        except Exception as e:
            return e
    elif type_info == 'country':
        try:
            url = "https://geocode-maps.yandex.ru/1.x/"
            params = {
                'geocode': city_name,
                'format': 'json'
            }
            data = requests.get(url, params).json()
            return data['response']['GeoObjectCollection']['featureMember'][0][
                'GeoObject']['metaDataProperty']['GeocoderMetaData'][
                'AddressDetails']['Country']['CountryName']
        except Exception as e:
            return e


def get_distance(p1, p2):
    radius = 6373.0

    lon1 = math.radians(p1[0])
    lat1 = math.radians(p1[1])
    lon2 = math.radians(p2[0])
    lat2 = math.radians(p2[1])

    d_lon = lon2 - lon1
    d_lat = lat2 - lat1

    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * \
                                   math.cos(lat2) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(a ** 0.5, (1 - a) ** 0.5)

    distance = radius * c
    return distance


def get_calculation(cities):
    if not cities:
        res['response']['text'] = 'Ты не написал название не одного города!'
    elif len(cities) == 1:
        res['response']['text'] = 'Этот город в стране - ' + \
                                  get_geo_info(cities[0], 'country')
    elif len(cities) == 2:
        distance = get_distance(get_geo_info(cities[0], 'coordinates'), get_geo_info(cities[1], 'coordinates'))
        res['response']['text'] = 'Расстояние между этими городами: ' + \
                                  str(round(distance)) + ' км.'
    else:
        res['response']['text'] = 'Слишком много городов!'
