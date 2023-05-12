from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol, connectionDone, ClientFactory
from twisted.internet import reactor, defer
from twisted.python import failure

import json


class Vehicle(Protocol):
    def connectionMade(self):
        print("Connected to the server!")

    def connectionLost(self, reason: failure.Failure = connectionDone):
        pass

    def dataReceived(self, data: bytes):
        # print("Got message: ", data.decode('utf-8'))
        if data is not None:
            reactor.callLater(0, self.parse_data, data)

    # 解析函数，提取有用参数

    def parse_data(self, data: bytes):
        vd_msg = json.loads('{}')
        vd_msg['passing_time'] = int.from_bytes(data[3:7], byteorder='big')
        vd_msg['line'] = int.from_bytes(data[7:8], byteorder='big')
        vd_msg['sum'] = int.from_bytes(data[8:10], byteorder='big')
        vd_msg['num_motor'] = int.from_bytes(data[10:12], byteorder='big')
        vd_msg['num_small_car'] = int.from_bytes(data[12:14], byteorder='big')
        vd_msg['num_big_car'] = int.from_bytes(data[14:16], byteorder='big')
        vd_msg['num_truck'] = int.from_bytes(data[16:18], byteorder='big')
        vd_msg['num_trailer'] = int.from_bytes(data[18:20], byteorder='big')
        vd_msg['average_speed'] = int.from_bytes(data[20:21], byteorder='big')
        vd_msg['speed_motor'] = int.from_bytes(data[21:22], byteorder='big')
        vd_msg['speed_small_car'] = int.from_bytes(data[22:23], byteorder='big')
        vd_msg['speed_big_car'] = int.from_bytes(data[23:24], byteorder='big')
        vd_msg['speed_truck'] = int.from_bytes(data[24:25], byteorder='big')
        vd_msg['speed_trailer'] = int.from_bytes(data[25:26], byteorder='big')
        vd_msg['average_car_spacing'] = int.from_bytes(data[26:28], byteorder='big')
        vd_msg['average_car_length'] = int.from_bytes(data[28:30], byteorder='big')
        vd_msg['average_occupancy'] = int.from_bytes(data[30:32], byteorder='big')

        print(vd_msg['passing_time'])


class VehicleClientFactory(ClientFactory):
    def __int__(self):
        self.protocol = None

    def startedConnecting(self, connector):
        print('Stated to connect')

    def buildProtocol(self, addr: IAddress) -> "Optional[Protocol]":
        self.protocol = Vehicle()
        return self.protocol

    def clientConnectionFailed(self, connector, reason):
        print('Lost connection. Reason:', reason)

    def clientConnectionLost(self, connector, reason):
        print('Connection failed. Reason:', reason)
