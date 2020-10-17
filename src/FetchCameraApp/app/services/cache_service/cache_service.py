from aiohttp import ClientSession

class CacheService:
    def __init__(self, client_session: ClientSession, url):
        self.client_session = client_session
        self.url = url

    async def create(self, id, value):
        params = { "key": id }
        return self.client_session.put(url=self.url, data=value, params=params)

    async def get(self, id):
        params = { "key": id }
        return self.client_session.get(url=self.url, params=params)

    async def update(self, id, value):
        params = { "key": id }
        return self.client_session.post(url=self.url, data=value, params=params)
    