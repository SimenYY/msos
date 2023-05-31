import json

from twisted.internet.protocol import Protocol, ReconnectingClientFactory, connectionDone
from twisted.internet import reactor, threads
from twisted.python import failure
from common.sansi import check


class VMSProtocol(Protocol):

    def __init__(self):
        with open('./device/vms/vms.json', 'r') as f:
            vms_config = json.load(f)
        self.get_current_display_msg = vms_config['get_current_display_msg']

    def connectionMade(self):
        print("Connected to the server")
        # run code in non-reactor thread
        reactor.callInThread(self.get_current_display)

    def dataReceived(self, data: bytes):
        reactor.callInThread(self.parse_data, data)

    def connectionLost(self, reason: failure.Failure = connectionDone):
        print("Disconnected from the server!")

    def get_current_display(self):
        import time
        while True:
            self.transport.write(bytes.fromhex(self.get_current_display_msg))
            time.sleep(1)
        # reactor.callLater(1, self.get_current_display)

    def parse_data(self, data: bytes):
        """
        帧头：1 字节，0x02，表明一帧的开始，为接收方提供同步。
        地址：2 字节，0x00,0x00 。
        帧数据： 序号 3 字节 ASCII 码，当前显示内容在播放表中的序号
               停留时间 5 字节 ASCII 码，当前显示内容的停留时间
               出字方式 2 字节 ASCII 码，当前显示内容的出字方式
               出字速度 5 字节 ASCII 码，当前显示内容的出字速度
               显示字符串 不定长 ASCII 码字符串，当前正在显示的内容，带转义符
        帧校验：2 字节，供接收方判断所收帧的正确性。帧校验采用 16 位的
               CRC 校验，生成多项式为 G(X) = X^16 + X^12 + X^5 + 1，计算范围包
               括地址、帧类型和未经转义的帧数据，算法见附录。发送时先发高字节，
               后发低字节。
        帧尾：1 字节，0x03，表明一帧的结束，为接收方提供同步。
        """
        start_data = b'\x02'
        end_data = b'\x03'
        is_data = False

        # 根据帧头帧尾提取内容，并转义
        for byte in data:
            if byte == start_data[0]:
                buffer = bytearray()
                is_data = True
            elif byte == end_data[0]:
                processed_data = check.un_transferred_meaning(buffer)
                buffer = bytearray()
                is_data = False
            elif is_data:
                buffer.append(byte)

            duration_of_stay = processed_data[5:10]
            out_way = processed_data[10:12]
            out_speed = processed_data[12:17]
            content = processed_data[17:-2]

            # 这里没有crc校验


class VMSClientFactory(ReconnectingClientFactory):
    protocol = VMSProtocol()

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

