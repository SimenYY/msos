# coding=utf-8
from twisted.internet.protocol import Protocol, ReconnectingClientFactory, connectionDone
from twisted.internet import reactor
from twisted.python import failure
import time
import json
import logging

"""
You can learn to build clients from https://docs.twisted.org/en/stable/core/howto/clients.html.
"""


class PhoneProtocol(Protocol):
    def __init__(self):
        # 存数据的变量
        self.data = {}

    def connectionMade(self):
        print("Connected to the server")

    def dataReceived(self, data: bytes):
        # 异步调用解析函数
        reactor.callInThread(self.parse_data, data)

    def connectionLost(self, reason: failure.Failure = connectionDone):
        print("Disconnected from the server!")

    # 解析函数，提取有用参数
    def parse_data(self, data: bytes):
        pass


class PhoneClientFactory(ReconnectingClientFactory):
    protocol = PhoneProtocol()

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