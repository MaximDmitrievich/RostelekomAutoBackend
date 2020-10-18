from os import environ
from aiohttp.web import Application, AppRunner, TCPSite
from asyncio import get_event_loop
from logging import INFO, getLogger
from pymongo import MongoClient
from middlewares.exception_handler_middleware import ExceptionHandlerMiddleware
from controllers.user_controller import UserController
from controllers.camera_controller import CameraController
from controllers.parking_controller import ParkingsController

if __name__ == "__main__":

    logger = getLogger(environ['APP_NAME'])
    logger.setLevel(INFO)

    middleware = ExceptionHandlerMiddleware(logger)

    mongo_client = MongoClient(host=environ["MONGODB_HOST"], port=int(environ["MONGODB_PORT"]), username=environ["MONGODB_LOGIN"], password=environ["MONGODB_PASSWORD"])

    user_controller = UserController(mongo_client)
    parkings_controller = ParkingsController(mongo_client)
    camera_controller = CameraController(mongo_client)

    application = Application(middlewares=[middleware.logging], logger=logger)

    async def main():
        application.router.add_get('/users', user_controller.get)
        application.router.add_get('/parkings', parkings_controller.get)
        application.router.add_get('/cameras', camera_controller.get)

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