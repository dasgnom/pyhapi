import requests
import json
from . import networks


class Station():
    """
    Find stations within the network.
    Either by name or by coordinates.
    """

    def __init__(self, network, apikey=False):
        self.accessId = apikey
        self.network = network


    def searchName(self, search, lon=False, lat=False, radius=1000, type='all', maxstop=5):
        """
        Find a station by name
        :param lon: longitude to search around in decimal format // TODO
        :param lat:  latitude to search around in decimal format // TODO
        :param radius: search radius in meters around coordinate // TODO
        :param type: Filter for location type //TODO
        :param maxstops: maximum number of stops to return
        :param products: hafas product bitmask // TODO
        :return: list of dicts with station details
        """

        url = networks.networks[self.network]['url']
        url += 'location.name'
        params = {}
        if self.accessId:
            params['accessId'] = self.accessId
        params['input'] = search.strip()
        params['format'] = 'json'
        params['maxNo'] = maxstop

        data = requests.get(url, params)

        if data.status_code != 200:
            raise ConnectionError from ConnectionError

        else:
            stationList  = data.content.decode('utf-8')
            return json.loads(stationList)

    def searchCoordinate(self, lat, lon, radius=1000):
        """
        Find stations around a location
        :param lon: longitude of center of search in decimal format
        :param lat: latitude of center of search in decimal format
        :param radius: search radius around given coordinate
        :param products: hafas product bitmask // TODO
        :return: list of dicts with station details
        """

        url = networks.networks[self.network]['url']
        url += 'location.nearbystops'
        params = {}
        params['accessId'] = self.accessId
        params['originCoordLat'] = float(lat)
        params['originCoordLong'] = float(lon)
        params['products'] = 255
        params['r'] = radius
        params['format'] = 'json'

        data = requests.get(url, params)

        if data.status_code == 401:
            raise ConnectionRefusedError from ConnectionError
        elif data.status_code != 200:
            raise ConnectionError from ConnectionError

        else:
            stationList = data.content.decode('utf-8')
            return json.loads(stationList)