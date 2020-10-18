from os import environ
from aiohttp.web import Application, AppRunner, TCPSite
from asyncio import get_event_loop
from logging import INFO, getLogger

from services.geolocation_service import GeolocationService
from services.db_provider import DBProvider
from middlewares.exception_handler_middleware import ExceptionHandlerMiddleware
from controllers.geolocation_controller import GeolocationController
from services.cache_service import CacheService

import pytz

if __name__ == "__main__":

    logger = getLogger(environ['APP_NAME'])
    logger.setLevel(INFO)

    middleware = ExceptionHandlerMiddleware(logger)
    geoloc = GeolocationService(environ['GEOLOCATOR_AGENT'])

    async def main():
        async with ClientSession() as client_session:
            cacher = CacheService(client_session, "http://{}:{}/redis".format(environ["CACHE_HOST"], environ["CACHE_PORT"]))
            db_provider = DBProvider(client_session, "http://{}:{}/".format(environ["DB_HOST"], environ["DB_PORT"]))
            controller = GeolocationController(db_provider, cacher, geoloc)

            application = Application(middlewares=[middleware.logging], logger=logger)
            application.router.add_get('/geocontroller/coords', controller.get_by_coords)
            application.router.add_get('/geocontroller/address', controller.get_by_address)

            runner = AppRunner(application)
            await runner.setup()
            site = TCPSite(runner, environ['APP_HOST'], int(environ['APP_PORT']))
            await site.start()

    loop = get_event_loop()
    try:
        loop.run_until_complete(main())
    except RuntimeError as exc:
        raise(exc)
    finally:
        loop.run_forever()