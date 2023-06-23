from apps import BroadcastProtocol, SendHelper
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.web.client import HTTPConnectionPool, Agent
from twisted.web.server import Site
from twisted.web.resource import Resource
import base_req
import datetime


class Drive(Resource):

    def __init__(self):
        super().__init__()
        self.token = base_req.get_token()
        self.refresh_time = datetime.datetime.now()
        self.task_list = base_req.get_task_status(self.token)

    def render_GET(self, request):
        request.setHeader(b"content-type", b"application/json")

        # 超过1h，刷新一下token
        current_time = datetime.datetime.now()
        time_diff = current_time - self.refresh_time
        if time_diff.total_seconds() > 3600:
            self.token = base_req.refresh_token(self.token)
            self.refresh_time = current_time

        id_status = base_req.get_terminal_status(self.token)

        return json.dumps(id_status).encode("utf-8")

    def render_POST(self, request):
        """
        [
          {
            "deviceCode": "BROADCAST_3",
            "content": {
              "flag": 1, //开关标志位，1开启，0关闭
              "play_mode": "normal_mode", //播放模式，"normal_mode":单次播放;"list_cycle_mode":循环播放
              "volume": 50, //音量，0-100
              "music_id_list": [1,2,3] //媒体列表
            }
          }
        ]
        :param request:
        :return:
        """
        current_time = datetime.datetime.now()
        time_diff = current_time - self.refresh_time
        if time_diff.total_seconds() > 3600:
            self.token = base_req.refresh_token(self.token)
            self.refresh_time = current_time

        request.setHeader(b"content-type", b"application/json")
        body = request.content.read()
        devices = None
        try:
            devices = json.loads(body)
        except json.JSONDecodeError:
            pass

        # metro-view与广播ID对应表
        with open("./comparison_table.json", "r") as t:
            table = json.load(t)

        endpoints_list = []
        music_list = devices[0]["content"]["music_id_list"]
        volume = devices[0]["content"]["volume"]
        action = devices[0]["content"]["flag"]
        play_mode = devices[0]["content"]["play_mode"]
        for device in devices:
            endpoints_list.append(int(table[device["deviceCode"]][10:]))
        if action == 1:  # 打开终端
            ret = base_req.set_mp3_play(self.token, music_list, endpoints_list, volume, play_mode, )
            if ret["result"] == 200:
                self.task_list = base_req.get_task_status(self.token)
                return str(ret).encode('utf-8')
            else:
                return str(ret).encode('utf-8')
        elif action == 0:  # 关闭终端
            for task in self.task_list:
                to_close_ep = []
                for ep in endpoints_list:
                    for Endpoint in task["EndpointIpList"]:
                        if ep == Endpoint["EndPointID"]:
                            to_close_ep.append(ep)
                if len(to_close_ep) == len(task["EndpointIpList"]):
                    ret = base_req.stop_task(self.token, task["TaskID"])
                else:
                    ret = base_req.remove_endpoints(self.token, task["TaskID"], to_close_ep)
            if ret["result"] == 200:
                self.task_list = base_req.get_task_status(self.token)
                return str(ret).encode('utf-8')
            else:
                return str(ret).encode('utf-8')

        return b"Hello, this is the control API."


root = Resource()
api = Resource()

root.putChild(b"api", api)
api.putChild(b"data", Drive())
api.putChild(b"control", Drive())
factory = Site(root)

pool = HTTPConnectionPool(reactor)
agent = Agent(reactor, pool=pool)

with open('./broadcast.json', 'r') as c:
    import json

    config = json.load(c)
metro_view_port = config["metro_view"]["port"]
ip_port = config["apps"]["ip_port"]

s = SendHelper(agent=agent, ip_port=ip_port)

reactor.listenTCP(metro_view_port, factory)
reactor.run()
