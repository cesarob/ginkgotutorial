import logging

import gevent

from ginkgo.core import Service, autospawn
from ginkgo.config import Setting

from .numbers import NumberClient
from .messaging.hub import MessageHub
from .messaging.websocket import WebSocketStreamer

logger = logging.getLogger(__name__)

class NumberGateway(Service):
    def __init__(self):
        self.client = NumberClient(('127.0.0.1', 7776))
        self.hub = MessageHub()
        self.ws = WebSocketStreamer(self.hub)

        self.add_service(self.hub)
        self.add_service(self.ws)
        self.add_service(self.client)

    def do_start(self):
        self._bridge()

    @autospawn
    def _bridge(self):
        for number in self.client:
            self.hub.publish('/numbers', number)
            gevent.sleep(0)
