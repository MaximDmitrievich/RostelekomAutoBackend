from aiohttp import ClientSession

class DBProvider:
    def __init__(self, uri: str, client_session: ClientSession):
        self.uri = uri
        self.client_session = client_session

    async def create(self, object, path):
        self.client_session