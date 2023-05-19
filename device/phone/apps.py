from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
import json


class PhoneProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onConnecting(self, transport_details):
        print("Connecting; transport details: {}".format(transport_details))
        return None  # ask for defaults

    def onOpen(self):
        print("WebSocket connection open.")

        def hello():
            self.sendMessage("Hello, world!".encode('utf8'))
            self.factory.reactor.callLater(1, hello)

        # start sending messages every second ..
        hello()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
            self.factory.reactor.callLater(0, self.parse_data, payload)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    def parse_data(self, data: bytes):
        data = json.loads(data.decode('utf8'))
        print("Parsed JSON data: {0}".format(data))
        if data["type"] == "event":
            phone_status = data["method"]


class PhoneClientFactory(WebSocketClientFactory):
    protocol = PhoneProtocol
