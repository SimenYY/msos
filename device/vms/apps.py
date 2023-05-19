from twisted.internet.protocol import Protocol, ReconnectingClientFactory, connectionDone
from twisted.internet import reactor
from twisted.python import failure


class VMSProtocol(Protocol):

    def connectionMade(self):
        print("Connected to the server")
        # 连接建立后发送查询报文
        self.get_current_display()

    def dataReceived(self, data: bytes):
        reactor.callLater(1, self.parse_data, data)

    def connectionLost(self, reason: failure.Failure = connectionDone):
        print("Disconnected from the server!")

    def get_current_display(self):
        self.transport.write(b"query")
        reactor.callLater(1, self.get_current_display)

    def parse_data(self, data: bytes):
        self.transport.write(b"parse_data")


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
