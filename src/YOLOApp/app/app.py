from os import environ
from aiohttp.web import Application, AppRunner, TCPSite
from asyncio import get_event_loop
from logging import INFO, getLogger
from middlewares.exception_handler_middleware import ExceptionHandlerMiddleware
from controllers.yolo_controller import YOLOController
from services.model_provider import ModelProvider
import tensorflow as tf

if __name__ == "__main__":
    my_devices = tf.config.experimental.list_physical_devices(device_type='CPU')
    tf.config.experimental.set_visible_devices(devices= my_devices, device_type='CPU')
    logger = getLogger(environ['APP_NAME'])
    logger.setLevel(INFO)

    middleware = ExceptionHandlerMiddleware(logger)

    model_provider = ModelProvider("outputs")

    controller = YOLOController(model_provider)

    application = Application(middlewares=[middleware.logging], logger=logger)

    async def main():    
        application.router.add_post('/detect', controller.post)

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