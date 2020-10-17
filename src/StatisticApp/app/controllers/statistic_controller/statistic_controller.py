import os
import json
import numpy as np

from aiohttp.web import Request, Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json, respond_with_html
from asyncio import get_event_loop, wait, shield
from concurrent.futures import ThreadPoolExecutor

from mainApp.controllers.statistic_controller.statistic_controller import StatisticController

class StatisticController(AioHTTPRestEndpoint):
    def __init__(self):
        self = self


    def get(self, request: Request) -> Response:
        return respond_with_json(status=200, data=json.dumps({"status": "OK", "code": 200, "Data": np.linspace(0, 20, 10)}))