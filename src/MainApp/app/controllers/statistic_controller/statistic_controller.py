import os

from aiohttp import ClientSession
from aiohttp.web import Request, Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json, respond_with_html
from asyncio import get_event_loop, wait, shield

class StatisticController(AioHTTPRestEndpoint):
    def __init__(self, statisic_provider):
        self.statistic_provider = statisic_provider

    async def get_statistic_on_time(self, request: Request) -> Response:
        if request.query is not None:
            long = request.query['longtitude']
            lat = request.query['latitude']
            time = request.query['time']
            