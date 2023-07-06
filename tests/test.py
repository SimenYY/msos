from protocol.phoneProtocolClientFactory import *
from twisted.internet import reactor

ph = PhoneProtocolClientFactory()
reactor.connectTCP("127.0.0.1", 8007, ph)
reactor.run()
