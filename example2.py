from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="nominatim.openstreetmap.org")
location = geolocator.reverse("55.81515422384692, 37.62904822826386")
print(location)
location2 = geolocator.geocode("")
print(location2)
print(geodesic((37.62904822826386, 55.81515422384692), (37.62362480163575, 55.812785087524446)).meters)