from twisted.internet import reactor, protocol, task


class QueryClient(protocol.Protocol):
    def connectionMade(self):
        self.sendQuery()

    def sendQuery(self):
        self.transport.write(b"query")
        # 每隔1秒发送一次查询报文
        reactor.callLater(1, self.sendQuery)

    def dataReceived(self, data):
        print("Received:", data)
        # 解析接收到的数据
        self.parseData(data)

    def connectionLost(self, reason):
        print("Connection lost:", reason.getErrorMessage())

    def parseData(self, data):
        # 在这里添加解析代码
        pass


class QueryClientFactory(protocol.ClientFactory):
    protocol = QueryClient

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost:", reason.getErrorMessage())
        reactor.stop()


if __name__ == '__main__':
    # 连接服务端
    reactor.connectTCP('localhost', 8000, QueryClientFactory())
    # 启动Reactor
    reactor.run()
