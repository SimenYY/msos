# -*- coding: utf-8 -*-
import json

from protocol.deviceProtocol import DeviceProtocol, Interval
from loguru import logger


class YoujiProtocol(DeviceProtocol):
    def connectionMade(self):
        self.login_ack()

    def dataReceived(self, data: bytes):
        super().dataReceived(data)

    def dataParse(self, data: bytes):
        logger.info(data)

    def login_ack(self):
        j = {}
        j['MSG'] = 6
        j['ack'] = 3
        j['type'] = 2
        j['flag'] = 0
        import time
        j['time'] = int(time.time())
        self.transport.write(json.dumps(j).encode('GB18030'))
