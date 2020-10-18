from aiohttp.web import Request, Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json, respond_with_html
from asyncio import get_event_loop, wait, shield
from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient
from bson.json_util import dumps

class ParkingsController(AioHTTPRestEndpoint):
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client
        self.db = self.mongo_client['RostelekomAuto']
        self.collection = self.db['Parkings']

    async def get(self, request: Request) -> Response:
        status = 500
        data = None
        collection = self.collection
        if collection is not None:
            if request.query is not None and len(request.query.keys()) > 0:
                entity = None
                print(request.query.keys())
                if 'id' in request.query:
                    id = request.query['id']
                    entity = self.collection.find_one(filter={u'_id': int(id)})
                elif 'camid' in request.query.keys():
                    id = request.query['camid']
                    entity = self.collection.find_one(filter={u'cameraid': int(id)})
                if entity is not None:
                    data = dumps(entity)
            else:
                data = dumps(list(collection.find()))
            if data is not None and data is not "" :
                status = 200
            else:
                status = 404
        return respond_with_json(status=status, data=data)