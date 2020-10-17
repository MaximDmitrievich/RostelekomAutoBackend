from os import environ
from aiohttp.web import Application, AppRunner, TCPSite
from asyncio import get_event_loop
from logging import INFO, getLogger
from .middlewares.exception_handler_middleware import ExceptionHandlerMiddleware
from .controllers.geolocation_controller import GeolocationController

import pytz

if __name__ == "__main__":

    logger = getLogger(environ['APP_NAME'])
    logger.setLevel(INFO)

    middleware = ExceptionHandlerMiddleware(logger)

    controller = GeolocationController()

    application = Application(middlewares=[middleware.logging], logger=logger)

    async def main():    
        application.router.add_get('/', controller.get)
        application.router.add_post('/entities', controller.post)

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