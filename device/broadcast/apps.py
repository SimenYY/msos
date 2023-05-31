from io import StringIO

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.web.client import ResponseDone

def handle_response(response):
    print("Response version:", response.version)
    print("Response code:", response.code)
    print("Response phrase:", response.phrase)
    print("Response headers:")
    for header, value in response.headers.getAllRawHeaders():
        print(header, value)
    finished = Deferred()
    response.deliverBody(BodyReceiver(finished))
    return finished

class BodyReceiver(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.remaining = 1024 * 10
        self.buffer = b""

    def dataReceived(self, bytes):
        if self.remaining:
            display = bytes[:self.remaining]
            self.buffer += display
            self.remaining -= len(display)

    def connectionLost(self, reason):
        if reason.check(ResponseDone):
            self.finished.callback(self.buffer)
        else:
            self.finished.errback(reason)

agent = Agent(reactor)
headers = Headers({'User-Agent': ['Twisted Web Client Example'], 'Content-Type': ['application/json']})
data = b'{"name": "Alice", "age": 25}'
d = agent.request(b'PUT', b'http://example.com/', headers=headers, bodyProducer=StringIO(data))
d.addCallback(handle_response)
d.addBoth(lambda _: reactor.stop())

reactor.run()