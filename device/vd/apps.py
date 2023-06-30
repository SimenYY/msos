from twisted.internet.protocol import Protocol, ReconnectingClientFactory, connectionDone
from twisted.internet import reactor
import json

from twisted.python import failure
import datetime

"""
You can learn to build clients from https://docs.twisted.org/en/stable/core/howto/clients.html.
"""


class VehicleProtocol(Protocol):

    def __init__(self):
        self.vd_msg = {}
        self.vd_msg["fast_line_5mins_traffic"] = 0
        self.vd_msg["fast_line_5mins_average_speed"] = 0
        self.vd_msg["fast_line_5mins_average_occupancy"] = 0
        self.vd_msg["fast_line_1h_traffic"] = 0
        self.vd_msg["fast_line_1h_average_speed"] = 0
        self.vd_msg["fast_line_1h_average_occupancy"] = 0
        self.vd_msg["mid_line_5mins_traffic"] = 0
        self.vd_msg["mid_line_5mins_average_speed"] = 0
        self.vd_msg["mid_line_5mins_average_occupancy"] = 0
        self.vd_msg["mid_line_1h_traffic"] = 0
        self.vd_msg["mid_line_1h_average_speed"] = 0
        self.vd_msg["mid_line_1h_average_occupancy"] = 0
        self.vd_msg["slow_line_5mins_traffic"] = 0
        self.vd_msg["slow_line_5mins_average_speed"] = 0
        self.vd_msg["slow_line_5mins_average_occupancy"] = 0
        self.vd_msg["slow_line_1h_traffic"] = 0
        self.vd_msg["slow_line_1h_average_speed"] = 0
        self.vd_msg["slow_line_1h_average_occupancy"] = 0

        self.msg = {}
        self.msg["fast_line_1h_traffic"] = 0
        self.msg["fast_line_1h_average_speed"] = 0
        self.msg["fast_line_1h_average_occupancy"] = 0
        self.msg["mid_line_1h_traffic"] = 0
        self.msg["mid_line_1h_average_speed"] = 0
        self.msg["mid_line_1h_average_occupancy"] = 0
        self.msg["slow_line_1h_traffic"] = 0
        self.msg["slow_line_1h_average_speed"] = 0
        self.msg["slow_line_1h_average_occupancy"] = 0

        self.time_5mins = datetime.datetime.now()
        self.time_1h = self.time_5mins

    def connectionMade(self):
        print("Connected to the server")

    def dataReceived(self, data: bytes):
        # 异步调用解析函数
        reactor.callInThread(1, self.parse_data, data)

    # 解析函数，提取有用参数
    def parse_data(self, data: bytes):
        # 车检器五分钟发清零前发一次报文
        current_time = datetime.datetime.now()
        print(current_time, self.transport.getPeer())
        print(data.hex())
        temp = {}
        while b'\xff\xf9\x1d' in data:
            start = data.find(b'\xff\xf9\x1d')
            single = data[start:start + 33]
            data = data[start + 33:]
            temp['line'] = int.from_bytes(single[7:8], byteorder='big', signed=False)
            temp["sum"] = int.from_bytes(single[8:10], byteorder='big', signed=False)
            temp["average_speed"] = int.from_bytes(single[20:21], byteorder='big', signed=False)
            temp["average_occupancy"] = int.from_bytes(single[30:32], byteorder='big', signed=False)

            # 1 快车道 2 中间车道 3 慢车道
            if temp["line"] == 0:
                self.vd_msg["fast_line_5mins_traffic"] += temp["sum"]
                self.vd_msg["fast_line_5mins_average_speed"] += temp["average_speed"]
                self.vd_msg["fast_line_5mins_average_occupancy"] += temp["average_occupancy"]
            elif temp["line"] == 1:
                self.vd_msg["mid_line_5mins_traffic"] += temp["sum"]
                self.vd_msg["mid_line_5mins_average_speed"] += temp["average_speed"]
                self.vd_msg["mid_line_5mins_average_occupancy"] += temp["average_occupancy"]
            elif temp["line"] == 2:
                self.vd_msg["slow_line_5mins_traffic"] += temp["sum"]
                self.vd_msg["slow_line_5mins_average_speed"] += temp["average_speed"]
                self.vd_msg["slow_line_5mins_average_occupancy"] += temp["average_occupancy"]

            if (current_time - self.time_1h).seconds <= 3600:
                # 1 快车道 2 中间车道 3 慢车道
                if temp["line"] == 0:
                    self.msg["fast_line_1h_traffic"] += temp["sum"]
                    self.msg["fast_line_1h_average_speed"] += temp["average_speed"]
                    self.msg["fast_line_1h_average_occupancy"] += temp["average_occupancy"]
                elif temp["line"] == 1:
                    self.msg["mid_line_1h_traffic"] += temp["sum"]
                    self.msg["mid_line_1h_average_speed"] += temp["average_speed"]
                    self.msg["mid_line_1h_average_occupancy"] += temp["average_occupancy"]
                elif temp["line"] == 2:
                    self.msg["slow_line_1h_traffic"] += temp["sum"]
                    self.msg["slow_line_1h_average_speed"] += temp["average_speed"]
                    self.msg["slow_line_1h_average_occupancy"] += temp["average_occupancy"]
            else:
                self.time_1h += datetime.timedelta(hours=1)
                self.vd_msg["fast_line_1h_traffic"] = self.msg["fast_line_1h_traffic"]
                self.vd_msg["fast_line_1h_average_speed"] = self.msg["fast_line_1h_average_speed"]
                self.vd_msg["fast_line_1h_average_occupancy"] = self.msg["fast_line_1h_average_occupancy"]
                self.vd_msg["mid_line_1h_traffic"] = self.msg["mid_line_1h_traffic"]
                self.vd_msg["mid_line_1h_average_speed"] = self.msg["mid_line_1h_average_speed"]
                self.vd_msg["mid_line_1h_average_occupancy"] = temp["average_occupancy"]
                self.vd_msg["slow_line_1h_traffic"] = self.msg["slow_line_1h_traffic"]
                self.vd_msg["slow_line_1h_average_speed"] = self.msg["slow_line_1h_average_speed"]
                self.vd_msg["slow_line_1h_average_occupancy"] = self.msg["slow_line_1h_average_occupancy"]
                self.msg["fast_line_1h_traffic"] = 0
                self.msg["fast_line_1h_average_speed"] = 0
                self.msg["fast_line_1h_average_occupancy"] = 0
                self.msg["mid_line_1h_traffic"] = 0
                self.msg["mid_line_1h_average_speed"] = 0
                self.msg["mid_line_1h_average_occupancy"] = 0
                self.msg["slow_line_1h_traffic"] = 0
                self.msg["slow_line_1h_average_speed"] = 0
                self.msg["slow_line_1h_average_occupancy"] = 0


        print(temp)
        print(self.vd_msg)
        return self.vd_msg

    def connectionLost(self, reason: failure.Failure = connectionDone):
        print("Disconnected from the server!")


class VehicleClientFactory(ReconnectingClientFactory):
    protocol = VehicleProtocol()

    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print('connected.')
        print('Resetting reconnection delay')
        self.resetDelay()
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
