from twisted.internet.protocol import Protocol, ReconnectingClientFactory, connectionDone
from twisted.internet import reactor
import json

from twisted.python import failure
import time

"""
You can learn to build clients from https://docs.twisted.org/en/stable/core/howto/clients.html.
"""



class LightingProtocol(Protocol):
    def __init__(self):
        self.vd_msg = {}

    def connectionMade(self):
        print("Connected to the server")
        reactor.callInThread(self.query_light_brightness)

    def query_light_brightness(self):
        while True:
            self.transport.write(b"\x00\x00\x00\x00\x00\x06\x01\x03\x05\x79\x00\x48")
            self.transport.write(b"\x00\x00\x00\x00\x00\x06\x01\x03\x05\xC1\x00\x48")
            time.sleep(2)
    def dataReceived(self, data: bytes):


        # 异步调用解析函数
        reactor.callInThread(self.parse_data, data)

    # 解析函数，提取有用参数
    def parse_data(self, data: bytes):
        print(data.hex())

    def connectionLost(self, reason: failure.Failure = connectionDone):
        print("Disconnected from the server!")


class LightingClientFactory(ReconnectingClientFactory):
    protocol = LightingProtocol()

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


lt = LightingClientFactory()
#reactor.connectTCP("172.16.11.19",1001, lt)
reactor.connectTCP("127.0.0.1",1001, lt)

reactor.run()