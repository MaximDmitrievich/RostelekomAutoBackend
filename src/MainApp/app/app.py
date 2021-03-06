from os import environ
from aiohttp import ClientSession
from aiohttp.web import Application, AppRunner, TCPSite
from asyncio import get_event_loop, ensure_future
from logging import INFO, getLogger

from services.yolo_provider import YOLOProvider
from services.geolocation_service import GeolocationService
from services.db_provider import DBProvider
from middlewares.exception_handler_middleware import ExceptionHandlerMiddleware
from controllers.geolocation_controller import GeolocationController
from services.cache_service import CacheService

if __name__ == "__main__":

    logger = getLogger(environ['APP_NAME'])
    logger.setLevel(INFO)

    middleware = ExceptionHandlerMiddleware(logger)
    geoloc = GeolocationService(environ['GEOLOCATOR_AGENT'])

    async def main(loop=None):
        cacher = CacheService(None, "http://{}:{}/redis".format(environ["CACHE_HOST"], environ["CACHE_PORT"]))
        db_provider = DBProvider(None, "http://{}:{}/".format(environ["DB_HOST"], environ["DB_PORT"]))
        yolo_provider = YOLOProvider(None, "http://{}:{}/".format(environ["YOLO_HOST"], environ["YOLO_PORT"]))
        controller = GeolocationController(db_provider, cacher, geoloc, yolo_provider)

        application = Application(middlewares=[middleware.logging], logger=logger)
        application.router.add_get('/geocontroller/coords', controller.get_by_coords)
        application.router.add_get('/geocontroller/address', controller.get_by_address)

        runner = AppRunner(application)
        await runner.setup()
        site = TCPSite(runner, environ['APP_HOST'], int(environ['APP_PORT']))
        await site.start()

    loop = get_event_loop()
    try:
        ensure_future(main(loop=loop), loop=loop)
        loop.run_forever()
    except RuntimeError as exc:
        logger.exception(exc)
        raise(exc)
    finally:
        loop.run_unitl_complete(main(loop=loop))
        loop.close()