import os

from aiohttp.web import Request, Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json, respond_with_html
from asyncio import get_event_loop, wait, shield
from concurrent.futures import ThreadPoolExecutor
from json import dumps

class YOLOController(AioHTTPRestEndpoint):
    def __init__(self, model_provider):
        self.model_provider = model_provider

    async def post(self, request: Request) -> Response:
        status = 500
        data = None
        if request.body_exists:
            body = await request.json()
            data = dumps(self.model_provider.detect(body['image']))
            if data is not None:
                status = 202
            else:
                status = 404
        return respond_with_json(status=status, data=data)