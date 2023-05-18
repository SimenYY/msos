from twisted.internet.protocol import Protocol, ReconnectingClientFactory, connectionDone
from twisted.internet import reactor
import json

from twisted.python import failure
import time

"""
You can learn to build clients from https://docs.twisted.org/en/stable/core/howto/clients.html.
"""


class VehicleProtocol(Protocol):

    def __init__(self):
        pass

    def connectionMade(self):
        print("Connected to the server")

    def dataReceived(self, data: bytes):

        # 异步调用解析函数
        reactor.callLater(1, self.parse_data, data)

    # 解析函数，提取有用参数
    def parse_data(self, data: bytes):
        with open('./device/vehicle/vehicle.json', 'r') as f:
            items = json.load(f)
        vd_msg = {}
        for item in items:
            # print(item["name"])
            value = int.from_bytes(data[item["index"]:item["index"] + item["sizeof"]], byteorder='big')
            vd_msg[item["name"]] = value
        print(vd_msg)

    def connectionLost(self, reason: failure.Failure = connectionDone):
        print("Disconnected from the server!")


class VehicleClientFactory(ReconnectingClientFactory):
    protocol = VehicleProtocol()

    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print('Connected.')
        print('Resetting reconnection delay')
        self.resetDelay()
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
