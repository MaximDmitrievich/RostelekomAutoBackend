from aiohttp import ClientSession

class DBProvider:
    def __init__(self, client_session: ClientSession, uri: str):
        self.uri = uri
        self.client_session = client_session

    async def __get__(self, path, param_name=None, id=None):
        if param_name is None or id is None:
            return self.client_session.get(self.uri + path)
        else:
            params={param_name : id }
            return self.client_session.get(self.uri + path, params=params)

    async def get_cameras(self, param_name=None, id=None):
        return self.__get__('cameras', param_name, id)
    
    async def get_parkings(self, param_name=None, id=None):
        return self.__get__('parkings', param_name, id)

    async def get_users(self, param_name=None, id=None):
        return self.__get__('users', param_name, id)
        
        