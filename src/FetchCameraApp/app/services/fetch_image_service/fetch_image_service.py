from aiohttp import ClientSession, ClientResponse
from models.db_models import Camera
from collections.abc import Iterable

class FetchImageService:
    def __init__(self, client_session: ClientSession, cameras):
        self.client_session = client_session
        self.cameras = cameras

    async def fetch_images(self):
        result = []
        for camera in self.cameras:
            print(camera.url)
            response: ClientResponse = await self.client_session.get(camera.url)
            camera.b64str = response.json()
            result.append(camera)
        return result