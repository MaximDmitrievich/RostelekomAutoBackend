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
            lat = float(request.query["lat"])
            long = float(request.query["long"])
            radius = float(request.query["max_radius"])
            cameras = loads(await self.db_provider.get_cameras())
            for camera in cameras:
                if self.geolocation_service.get_circle(long, lat, camera['long'], camera['lat']) > radius:
                    cameras.remove(camera)

            for camera in cameras:
                parkings = loads(await self.db_provider.get_parkings(param_name='camid', id=int(camera['_id'])))
                free_places = 4
                result += list(map(lambda x: {"long": float(x['long']), "lat": float(x['lat']), "free_places": free_places }, parkings))
        return respond_with_json(status=200, data=result)

    async def get_by_address(self, request: Request) -> Response:
        result = []
        if request.query is not None:
            address = request.query["address"]
            lat, long = self.geolocation_service.get_address(address)
            radius = float(request.query["max_radius"])
            cameras = loads(await self.db_provider.get_cameras())
            for camera in cameras:
                if self.geolocation_service.get_circle(long, lat, camera['long'], camera['lat']) > radius:
                    cameras.remove(camera)                

            for camera in cameras:
                parkings = loads(await self.db_provider.get_parkings(param_name='camid', id=int(camera['_id'])))
                result.append(list(map(lambda x: {"long": x['long'], "lat": x['lat'], "free_places": 4 }, parkings)))
        return respond_with_json(status=200, data=result)