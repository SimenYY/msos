import time

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.python import failure
from twisted.web.client import Agent
from twisted.internet.protocol import Protocol, connectionDone
from twisted.web.http_headers import Headers
from pprint import pformat
from twisted.internet.task import LoopingCall
from bytesprod import BytesProducer

"""
1. GET 获取token 
http://172.16.11.26:8001/api/v29+/auth?name=admin&password=123456G
2. GET 刷新token
http://172.16.11.26:8001/api/v29+/auth/refresh
3. PUT 获取终端信息
http://172.16.11.26:8001/api/v29+/ws/forwarder

    body:
    {
        "company" : "BL", 
        "actioncode" : "c2ls_get_server_terminals_status",
        "token" :
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTg1ODE5NzQsImlhdCI6MT
            U5ODU3NDQ3NCwiaXNzIjoiSVAiLCJwbGF0Zm9ybSI6IndlYiIsInN1YiI6ImFsbCIsInR5cC
            I6IkpXVCIsInVzZXJzX2lkIjo1fQ.RwYKOSq6Eir2DyJXIWVQq7bdBxpkdyONLwx6kDuSDrk", 
        "data" : "",
        "result" : 200, 
        "return_message" : "",
        "sign" : "rand string"
    }
"""


class BroadcastProtocol(Protocol):
    def __init__(self, finished):
        self.finished = finished

    def dataReceived(self, data: bytes):
        print(data)

    def connectionLost(self, reason: failure.Failure = connectionDone):
        print("Finished receiving body:", reason.getErrorMessage())
        self.finished.callback(None)


headers = Headers({
    "User-Agent": ["Twisted Web Client"],
    "Content-Type": ["application/json; charset=utf-8"]
})

agent = Agent(reactor)


def get_token():
    d = agent.request(
        b"GET",
        b"http://127.0.0.1:8001/api/v29+/auth?name=admin&password=123456",
        headers=headers
    )
    d.addCallback(cdResponse)


def refresh_token():
    d = agent.request(
        b"GET",

    )


def get_terminal_info():
    pass


def cdResponse(response):
    print("Response version:", response.version)
    print("Response code:", response.code)
    print("Response phrase:", response.phrase)
    print("Response headers:")
    print(pformat(list(response.headers.getAllRawHeaders())))
    finished = Deferred()
    response.deliverBody(BroadcastProtocol(finished))
    return finished


def cbBody(body):
    print("Response body:")
    print(body)


reactor.run()
