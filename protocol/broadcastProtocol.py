# -*- coding: utf-8 -*-

from protocol.deviceProtocol import DeviceProtocol, Interval
from data.value import value_dic


class BroadcastProtocol(DeviceProtocol):
    def dataReceived(self, data: bytes):
        super().dataReceived(data)

    def dataParse(self, data: bytes):
        pass

    @Interval('1/second')
    def heart_beat(self):
        pass

    def connectionMade(self):
        print(self.transport.getPeer())



