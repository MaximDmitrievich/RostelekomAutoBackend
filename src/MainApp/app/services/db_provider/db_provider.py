from aiohttp import ClientSession, ClientResponse

class DBProvider:
    def __init__(self, client_session: ClientSession, uri: str):
        self.uri = uri
        self.client_session = client_session

    async def __get__(self, path, param_name=None, id=None):
        if param_name is None or id is None:
            if self.client_session is None:
                async with ClientSession() as session:
                    response: ClientResponse = await session.get(self.uri + path)
            else:
                response: ClientResponse = await self.client_session.get(self.uri + path)
            return await response.json()
        else:
            params={param_name : id }
            if self.client_session is None:
                async with ClientSession() as session:
                    response: ClientResponse = await session.get(self.uri + path, params=params)
            else:
                response: ClientResponse = await self.client_session.get(self.uri + path, params=params)            
            return await response.json()

    async def get_cameras(self, param_name=None, id=None):
        response = await self.__get__('cameras', param_name, id)
        return response
    
    async def get_parkings(self, param_name=None, id=None):
        response = await self.__get__('parkings', param_name, id)
        return response

    async def get_users(self, param_name=None, id=None):
        response: ClientResponse = await self.__get__('users', param_name, id)
        return response
        
        