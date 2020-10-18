from logging import INFO, getLogger
from aiohttp import ClientSession
from asyncio import get_event_loop, sleep, Semaphore, ensure_future, gather
from operator import add
from os import environ
from json import dumps

from services.fetch_image_service import FetchImageService
from services.cache_service import CacheService
from models.db_models import Camera
#http://c001.sm0t.ru/?d=1602925163707

if __name__ == "__main__":
    cameras = []
    cameras.append(Camera(id=1, long=37.62904822826386, lat=55.81515422384692, url='http://91.233.230.14/jpg/image.jpg', address="Россия Москва, Звёздный бульвар"))
    logger = getLogger(environ['APP_NAME'])    

    async def looped(loop=None):
        async with ClientSession() as client_session:
            fetcher = FetchImageService(client_session, cameras)
            cacher = CacheService(client_session, "http://{}:{}/redis".format(environ["CACHE_HOST"], environ["CACHE_PORT"]))
            while True:
                try:
                    photos = await fetcher.fetch_images()
                    for photo in photos:
                        await cacher.update(photo.id, photo.b64str)
                except Exception as exc:
                    logger.exception(exc)
                await sleep(5, loop=loop)

    loop = get_event_loop()
    try:
        ensure_future(looped(loop=loop), loop=loop)
        loop.run_forever()
    except RuntimeError as exc:
        logger.exception(exc)
        raise(exc)
    finally:
        loop.run_unitl_complete(looped(loop=loop))
        loop.close()