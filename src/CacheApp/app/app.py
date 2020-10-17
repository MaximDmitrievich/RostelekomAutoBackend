from os import environ
from aiohttp.web import Application, AppRunner, TCPSite
from asyncio import get_event_loop
from logging import INFO, getLogger
from redis.client import Redis
from middlewares.exception_handler_middleware import ExceptionHandlerMiddleware
from controllers.cache_controller import CacheController

if __name__ == "__main__":

    logger = getLogger(environ['APP_NAME'])
    logger.setLevel(INFO)

    middleware = ExceptionHandlerMiddleware(logger)

    application = Application(middlewares=[middleware.logging], logger=logger)

    redis_client = Redis(host=environ['CACHE_HOST'], port=environ['CACHE_PORT'], decode_responses=True)

    controller = CacheController(redis_client)

    async def main():    
        application.router.add_get('/redis', controller.get)
        application.router.add_put('/redis', controller.put)
        application.router.add_post('/redis', controller.post)
        application.router.add_delete('/redis', controller.delete)

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