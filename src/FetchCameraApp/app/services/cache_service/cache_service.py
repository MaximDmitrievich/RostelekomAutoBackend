from aiohttp import ClientSession
from json import dumps

class CacheService:
    def __init__(self, client_session: ClientSession, url):
        self.client_session = client_session
        self.url = url

    async def create(self, id, value):
        params = { "key": id }
        headers= {'content-type': 'application/json'}
        return await self.client_session.put(url=self.url, json={ "image": str(value) }, params=params, headers=headers)

    async def get(self, id):
        params = { "key": id }
        return await self.client_session.get(url=self.url, params=params)

    async def update(self, id, value):
        params = { "key": id }
        headers= {'content-type': 'application/json'}
        return await self.client_session.post(url=self.url, json={ "image": str(value) }, params=params, headers=headers)
    