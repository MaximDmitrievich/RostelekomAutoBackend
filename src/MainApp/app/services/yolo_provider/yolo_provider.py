from aiohttp import ClientSession
from json import dumps

class YOLOProvider:
    def __init__(self, client_session: ClientSession, url):
        self.client_session = client_session
        self.url = url

    async def get(self, data):
        if self.client_session is None:
            async with ClientSession() as session:
                response = await session.post(url=self.url, data=data)
        else:
            response = await self.client_session.post(url=self.url, data=data)
        return response
    