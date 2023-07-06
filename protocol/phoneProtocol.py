from twisted.internet.protocol import Protocol, connectionDone
from twisted.python import failure
from twisted.internet import reactor


class PhoneProtocol(Protocol):
    def __init__(self):
        pass

    def connectionMade(self):
        pass

    def connectionLost(self, reason: failure.Failure = connectionDone):
        pass

    def dataReceived(self, data: bytes):
        return reactor.callInThread(self.parse, data)

    def parse(self, data: bytes):
        pass



