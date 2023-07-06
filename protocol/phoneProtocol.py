from twisted.internet.protocol import Protocol, ReconnectingClientFactory, connectionDone
from twisted.python import failure


class PhoneProtocol(Protocol):
    def __init__(self):
        pass

    def connectionMade(self):
        pass

    def connectionLost(self, reason: failure.Failure = connectionDone):
        pass

    def dataReceived(self, data: bytes):
        pass

    class PhoneProtocolFactory(ReconnectingClientFactory):
        pass

