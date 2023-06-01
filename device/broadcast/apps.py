import json

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.python import failure
from twisted.web.client import Agent
from twisted.internet.protocol import Protocol, connectionDone
from twisted.web.http_headers import Headers
from pprint import pformat
from twisted.internet.task import LoopingCall
from bytesprod import BytesProducer


class BroadcastProtocol(Protocol):
    def __init__(self, finished):
        self.finished = finished

    def dataReceived(self, data: bytes):
        reactor.callInThread(self.parse_data, data)

    def connectionLost(self, reason: failure.Failure = connectionDone):
        print("Finished receiving body:", reason.getErrorMessage())
        self.finished.callback(None)

    def parse_data(self, data: bytes):
        pass


headers = Headers({
    "User-Agent": ["Twisted Web Client"],
    "Content-Type": ["application/json; charset=utf-8"]
})

agent = Agent(reactor)
ip_port = "127.0.0.1:8001"


def get_token():
    """
    GET 获取token
        http://172.16.11.26:8001/api/v29+/auth?name=admin&password=123456G
    :return:
    """
    path = "/api/v29+/auth?name=admin&password=123456"
    url = "http://" + ip_port + path
    d = agent.request(b"GET", url.encode('utf-8'), headers=headers)
    d.addCallback(cdResponse)


def refresh_token():
    """
    GET 刷新token
        http://172.16.11.26:8001/api/v29+/auth/refresh
    :return:
    """
    path = "/api/v29+/auth/refresh"
    url = "http://" + ip_port + path
    d = agent.request(b"GET", url.encode('utf-8'), headers=headers)
    d.addCallback(cdResponse)


def get_terminal_info():
    """
    PUT 获取终端信息
        http://172.16.11.26:8001/api/v29+/ws/forwarder

        body:
        {
            "company" : "BL",
            "actioncode" : "c2ls_get_server_terminals_status",
            "token" : "",
            "data" : "",
            "result" : 200,
            "return_message" : "",
            "sign" : "rand string"
        }
    :return:
    """
    path = "/api/v29+/ws/forwarder"
    url = "http://" + ip_port + path

    body = json.loads("{}")
    body["company"] = "BL"
    body["actioncode"] = "c2ls_get_server_terminals_status"
    body["token"] = None
    body["data"] = ""
    body["result"] = 200
    body["return_message"] = ""
    body["sign"] = "rand string"

    d = agent.request(b"PUT", url.encode('utf-8'), headers=headers, bodyProducer=body)
    d.addCallback(cdResponse)


def set_mp3_play():
    """
    PUT 点播服务器音乐（mp3播放）
        http://172.16.21.183:8001/api/v29+/ws/forwarder

        body:
        {
            "company" : "BL",
            "actioncode" : "c2ls_mobile_terminal_damand_music",
            "token" :"",
            "data" : {
                "EndPointsAdditionalProp": "",
                "EndPointIDs": [7,11],
                "EndPointGroupIDs" : [],
                "MusicIDs": [1, 3, 6],
                "MusicGroupIDs" : [],
                "TaskID": "{098ADF3F20E54AFAAE23AA5DB509176D}",
                "TaskName": "音乐_191016195004",
                "Priority": 70,
                "Volume": 50,
                "PlayMode" : "normal_mode"
            },
            "result" : 200,
            "return_message" : "",
            "sign" : "rand string"
        }
    :return:
    """
    path = "/api/v29+/ws/forwarder"
    url = "http://" + ip_port + path

    body = json.loads("{}")
    body["company"] = "BL"
    body["actioncode"] = "c2ls_mobile_terminal_damand_music"
    body["token"] = None
    body["data"] = {}
    body["data"]["EndPointsAdditionalProp"] = ""
    body["data"]["EndPointIDs"] = []
    body["data"]["EndPointGroupIDs"] = []
    body["data"]["MusicIDs"] = []
    body["data"]["MusicGroupIDs"] = []
    body["data"]["TaskID"] = ""
    body["data"]["TaskName"] = ""
    body["data"]["Priority"] = ""
    body["data"]["Volume"] = ""
    body["data"]["PlayMode"] = ""
    body["result"] = 200
    body["return_message"] = ""
    body["sign"] = "rand string"

    d = agent.request(b"PUT", url.encode('utf-8'), headers=headers, bodyProducer=body)
    d.addCallback(cdResponse)


def cdResponse(response):
    finished = Deferred()
    response.deliverBody(BroadcastProtocol(finished))
    return finished


get_token()

reactor.run()
