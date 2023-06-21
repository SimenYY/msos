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
        modbus_header = "\x00\x00\x00\x00\x00\x06"
        device_address = "\x01"
        func_code ="\x03"
        # 受报文返回长度限制，每次查询72个寄存器
        register_address_list = ["\x05\x79","\x05\xC1"]
        read_num = "\x00\x48"
        msg1 = ''.join([modbus_header, device_address,
                        func_code, register_address_list[0], read_num])
        msg2 = ''.join([modbus_header, device_address,
                        func_code, register_address_list[1], read_num])
        msg = ''.join([msg1, msg2])

        while True:
            self.transport.write(msg.encode())
            time.sleep(5)
    def dataReceived(self, data: bytes):


        # 异步调用解析函数
        reactor.callInThread(self.parse_data, data)

    # 解析函数，提取有用参数
    def parse_data(self, data: bytes):
        pass

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

