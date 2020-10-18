import os

from aiohttp.web import Request, Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json, respond_with_html
from asyncio import get_event_loop, wait, shield
from concurrent.futures import ThreadPoolExecutor
from services.geolocation_service import GeolocationService

class GeolocationController(AioHTTPRestEndpoint):
    def __init__(self, db_provider, geolocation_service: GeolocationService):
        self.db_provider = db_provider
        self.geolocation_service = geolocation_service

    async def get(self, request: Request) -> Response:
        if request.query is not None:
            latitude = request.query["latitude"]
            longtitude = request.query["longtitude"]
            radius = request.query["max_radius"]
            
        return 