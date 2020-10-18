from geopy.geocoders import Nominatim
from geopy.distance import geodesic, great_circle

class GeolocationService:
    def __init__(self, agent_name):
        self.geolocator = Nominatim(user_agent=agent_name)

    def get_coords(self, address):
        location = self.geolocator.geocode(address)
        return (location.latitude, location.longitude)

    def get_address(self, long, lat):
        location = self.geolocator.reverse("{}, {}".format(lat, long))
        return location.address

    def get_distance(self, long1, lat1, long2, lat2):
        return geodesic((long1, lat1), (long2, lat2)).meters

    def get_circle(self, long1, lat1, long2, lat2):
        return great_circle((long1, lat1), (long2, lat2)).meters