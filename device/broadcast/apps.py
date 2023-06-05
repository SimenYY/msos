import json

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.python import failure
from twisted.web.client import Agent, HTTPConnectionPool
from twisted.internet.protocol import Protocol, connectionDone
from twisted.web.http_headers import Headers
from pprint import pformat
from twisted.internet.task import LoopingCall
from bytesprod import BytesProducer


class BroadcastProtocol(Protocol):
    def __init__(self, finished):
        self.finished = finished

    def connectionMade(self):
        # 连接建立时可以做一些事情
        pass

    def dataReceived(self, data: bytes):
        reactor.callInThread(self.parse_data, data)

    def connectionLost(self, reason: failure.Failure = connectionDone):
        print("Finished receiving body:", reason.getErrorMessage())
        self.finished.callback(None)

    def parse_data(self, data: bytes):
        ret = json.loads(data)


pool = HTTPConnectionPool(reactor)
agent = Agent(reactor, pool=pool)
ip_port = "172.16.11.26:8001"


def get_token():
    """
    GET 获取token
        http://172.16.11.26:8001/api/v29+/auth?name=admin&password=123456G
    :return:
    """
    path = "/api/v29+/auth?name=admin&password=123456"
    url = "http://" + ip_port + path
    headers = Headers({
        "User-Agent": ["Twisted Web Client"],
        "Content-Type": ["application/json; charset=utf-8"]
    })
    d = agent.request(
        b"GET",
        url.encode('utf-8'),
        headers=headers)
    d.addCallback(cpResponse)


def refresh_token(old_token):
    """
    GET 刷新token
        http://172.16.11.26:8001/api/v29+/auth/refresh
    注：60mins 刷新一次
    :return:
    """
    headers = Headers({
        "User-Agent": ["Twisted Web Client"],
        "Content-Type": ["application/json; charset=utf-8"],
        "Authorization": [old_token]
    })
    path = "/api/v29+/auth/refresh"
    url = "http://" + ip_port + path
    d = agent.request(
        b"GET",
        url.encode('utf-8'),
        headers=headers)
    d.addCallback(cpResponse)


def get_terminal_info(token):
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
    body["token"] = token
    body["data"] = ""
    body["result"] = 200
    body["return_message"] = ""
    body["sign"] = "rand string"

    headers = Headers({
        "User-Agent": ["Twisted Web Client"],
        "Content-Type": ["application/json; charset=utf-8"]
    })
    d = agent.request(
        b"PUT",
        url.encode('utf-8'),
        headers=headers,
        bodyProducer=BytesProducer(json.dumps(body).encode('utf-8')))
    d.addCallback(cpResponse)


def set_mp3_play(EndPointIDs_list, MusicIDs_list, token):
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
    body["token"] = token
    body["data"] = {}
    body["data"]["EndPointsAdditionalProp"] = ""
    body["data"]["EndPointIDs"] = EndPointIDs_list
    body["data"]["EndPointGroupIDs"] = []
    body["data"]["MusicIDs"] = MusicIDs_list
    body["data"]["MusicGroupIDs"] = []
    from utils import generate_random_31_number
    task_id = "{" + generate_random_31_number() + "}"
    body["data"]["TaskID"] = task_id
    body["data"]["TaskName"] = ""
    body["data"]["Priority"] = ""
    body["data"]["Volume"] = ""
    body["data"]["PlayMode"] = ""
    body["result"] = 200
    body["return_message"] = ""
    body["sign"] = "rand string"

    headers = Headers({
        "User-Agent": ["Twisted Web Client"],
        "Content-Type": ["application/json; charset=utf-8"]
    })
    d = agent.request(
        b"PUT",
        url.encode('utf-8'),
        headers=headers,
        bodyProducer=BytesProducer(json.dumps(body).encode('utf-8')))
    d.addCallback(cpResponse)
    return task_id


def stop_task(task_id, token):
    """
    PUT 停止任务
    http://172.16.11.26:8001/api/v29+/ws/forwarder
        body
        {
        "company" : "BL",
        "actioncode" : "c2ls_stop_task",
        "token" : ",
        "data" : {
        "TaskID" : "{098ADF3F20E54AFAAE23AA5DB509176D}"
        },
        "result" : 200,
        "return_message" : "",
        "sign" : "rand string"
        }
    注意：TaskID 是用于区别任务的,由大括号加31位随机数组成,由调用方自己生成随机数
    :return:
    """
    path = "/api/v29+/ws/forwarder"
    url = "http://" + ip_port + path
    headers = Headers({
        "User-Agent": ["Twisted Web Client"],
        "Content-Type": ["application/json; charset=utf-8"]
    })

    body = json.loads("{}")
    body["company"] = "BL"
    body["actioncode"] = "c2ls_stop_task"
    body["token"] = token
    body["data"] = {}
    body["data"]["TaskID"] = task_id
    body["result"] = 200
    body["return_message"] = ""
    body["sign"] = "rand string"
    d = agent.request(
        b"PUT",
        url.encode('utf-8'),
        headers=headers,
        bodyProducer=BytesProducer(json.dumps(body).encode('utf-8')))
    d.addCallback(cpResponse)


def cpResponse(response):
    finished = Deferred()
    response.deliverBody(BroadcastProtocol(finished))
    return finished


get_token()
refresh_token()

reactor.run()
