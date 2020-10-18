from aiohttp.web import Request, Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json, respond_with_html
from asyncio import get_event_loop, wait, shield
from concurrent.futures import ThreadPoolExecutor
from redis import Redis
import json

class CacheController(AioHTTPRestEndpoint):
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def get(self, request: Request) -> Response:
        data = None
        status = 500
        if request.query is not None:
            key = request.query['key']
            value = self.redis_client.get(key)
            if value is not None:
                data = json.loads(value)
                status = 200
            else:
                status = 404
        return respond_with_json(status=status, data=data)
        

    async def put(self, request: Request) -> Response:
        data = None
        status = 500
        if request.body_exists and request.query is not None:
            body = await request.json()
            value_str = json.dumps(body)
            key = request.query['key']
            data = self.redis_client.set(key, value_str)
            if data is not None:
                status = 201
            else:
                status = 400
        return respond_with_json(status=status, data=data)

    async def post(self, request: Request) -> Response:
        data = None
        status = 500
        if request.body_exists and request.query is not None:
            body = await request.json()
            value_str = json.dumps(body)
            key = request.query['key']
            value = self.redis_client.get(key)
            data = None
            if value is not None:
                self.redis_client.delete(key)
                data = self.redis_client.append(key, value_str)
            else:
                data = self.redis_client.set(key, value_str)
            
            if data is not None:
                status = 201
            else:
                status = 400
        return respond_with_json(status=status, data=data)

    async def delete(self, request: Request) -> Response:
        data = None
        status = 500
        if request.query is not None:
            key = request.query['key']
            data = self.redis_client.delete(key)
            if data is not None:
                status = 202
            else:
                status = 404
        return respond_with_json(status=status, data=data)