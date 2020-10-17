from aiohttp import ClientSession, ClientResponse, MultipartReader
from models.db_models import Camera
from collections.abc import Iterable
from base64 import b64encode

class FetchImageService:
    def __init__(self, client_session: ClientSession, cameras):
        self.client_session = client_session
        self.cameras = cameras

    async def fetch_images(self):
        result = []
        for camera in self.cameras:
            response: ClientResponse = await self.client_session.get(camera.url)
            image_bytes = await response.read()
            b64 = b64encode(image_bytes)
            camera.b64str = b64
            result.append(camera)
        return result