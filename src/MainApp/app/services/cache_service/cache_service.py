from aiohttp import ClientSession
from json import dumps

class CacheService:
    def __init__(self, client_session: ClientSession, url):
        self.client_session = client_session
        self.url = url

    async def create(self, id, value):
        params = { "key": id }
        headers= {'content-type': 'application/json'}
        if self.client_session is None:
            async with ClientSession() as session:
                response = await session.put(url=self.url, json={ "image": str(value) }, params=params, headers=headers)
        else:
            response = await self.client_session.put(url=self.url, json={ "image": str(value) }, params=params, headers=headers)
        return response

    async def get(self, id):
        params = { "key": id }
        if self.client_session is None:
            async with ClientSession() as session:
                response = await session.get(url=self.url, params=params)
        else:
            response = await self.client_session.get(url=self.url, params=params)
        return response

    async def update(self, id, value):
        params = { "key": id }
        headers= {'content-type': 'application/json'}
        if self.client_session is None:
            async with ClientSession() as session:
                response = await session.post(url=self.url, json={ "image": str(value) }, params=params, headers=headers)
        else: 
            response = await self.client_session.post(url=self.url, json={ "image": str(value) }, params=params, headers=headers)
        return response
    