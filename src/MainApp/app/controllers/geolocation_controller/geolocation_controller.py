import os

from aiohttp.web import Request, Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json, respond_with_html
from asyncio import get_event_loop, wait, shield
from concurrent.futures import ThreadPoolExecutor
from services.geolocation_service import GeolocationService
from services.db_provider import DBProvider
from services.cache_service import CacheService
from json import loads, dumps

class GeolocationController(AioHTTPRestEndpoint):
    def __init__(self, db_provider: DBProvider, cacher: CacheService, geolocation_service: GeolocationService):
        self.db_provider = db_provider
        self.geolocation_service = geolocation_service
        self.cacher = cacher

    async def get_by_coords(self, request: Request) -> Response:
        result = []
        if request.query is not None:
            lat = request.query["lat"]
            long = request.query["long"]
            radius = request.query["max_radius"]
            cameras = loads(self.db_provider.get_cameras())
            for camera in cameras:
                if self.geolocation_service.get_cirlce(long, lat, camera.long, camera.lat) > radius:
                    cameras.remove(camera)

            for camera in cameras:
                parkings = loads(self.db_provider.get_parkings(param_name='camid', id=camera._id))
                result.append(list(map(lambda x: (x.long, x.lat), parkings)))
        return result

    async def get_by_address(self, request: Request) -> Response:
        result = []
        if request.query is not None:
            address = request.query["address"]
            lat, long = self.geolocation_service.get_address(address)
            radius = request.query["max_radius"]
            cameras = loads(self.db_provider.get_cameras())
            for camera in cameras:
                if self.geolocation_service.get_cirlce(long, lat, camera.long, camera.lat) > radius:
                    cameras.remove(camera)                

            for camera in cameras:
                parkings = loads(self.db_provider.get_parkings(param_name='camid', id=camera._id))
                result.append(list(map(lambda x: (x.long, x.lat), parkings)))
        return result