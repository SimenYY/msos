# -*- coding: utf-8 -*-

from protocol.deviceProtocol import DeviceProtocol, Interval


class BroadcastProtocol(DeviceProtocol):
    def dataReceived(self, data: bytes):
        super().dataReceived(data)

    def dataParse(self, data: bytes):
        from loguru import logger
        logger.info(data)
        pass

    @Interval('2/second')
    def send(self):
        data = b'1'
        self.transport.write(data)

    def connectionMade(self):
        from twisted.internet import reactor
        reactor.callInThread(self.send)
