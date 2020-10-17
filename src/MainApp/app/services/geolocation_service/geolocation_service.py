from math import radians, cos, sin, asin, sqrt
from yandex_maps import api

class GeolocationService:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_geocode(self, address):
        return api.geocode(self.api_key, address=address)

    def get_address(self, longtitude, latitude):
        return api.get_map_url(api_key=self.api_key, longitude=longtitude, latitude=latitude, zoom=13, width=300, height=300)