from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import ReconnectingClientFactory
from broadcastProtocol import *
from typing import Optional


class BroadcastProtocolClientFactory(ReconnectingClientFactory):
    protocol = BroadcastProtocol()

    def buildProtocol(self, addr: IAddress) -> "Optional[Protocol]":
        self.resetDelay()
        return self.protocol

    def clientConnectionFailed(self, connector, reason):
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, unused_reason):
        ReconnectingClientFactory.clientConnectionLost(self, connector, unused_reason)
