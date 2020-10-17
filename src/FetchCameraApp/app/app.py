from logging import INFO, getLogger
from aiohttp import ClientSession
from asyncio import run, get_event_loop, set_event_loop
from operator import add
from os import environ
import json
from time import sleep

from services.fetch_image_service import FetchImageService
from services.cache_service import CacheService
from models.db_models import Camera

cameras = [
    Camera(id=1, long=37.6290409, lat=55.8151547, url='http://91.233.230.14/jpg/image.jpg', address="Россия Москва, Звёздный бульвар")
]

if __name__ == "__main__":
    logger = getLogger(environ['APP_NAME'])    

    async def looped(fetcher, cacher):
        try:
            photos = await fetcher.fetch_images()
            for photo in photos:
                cacher.update(photo.id, photo.b64str)
            sleep(60)
        except Exception as exc:
            logger.exception(exc.body)
            print(exc)


    async def main(loop=None):
        async with ClientSession() as client_session:
            fetcher = FetchImageService(client_session, cameras)
            cacher = CacheService(client_session, "http://{}:{}/redis".format(environ["CACHE_APP"], environ["CACHE_PORT"]))
            while True:
                result = await loop.run_in_executor(
                    None,  
                    looped,
                    fetcher, cacher)

    loop = get_event_loop()
    try:
        coro = main(loop)
        set_event_loop(loop)
        loop.run_until_complete(coro)
    finally:
        loop.run_forever()