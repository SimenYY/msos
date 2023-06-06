from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.web.client import HTTPConnectionPool, Agent
from twisted.web.server import Site
from twisted.web.resource import Resource


class Drive(Resource):

    def __init__(self):
        super().__init__()
        import requests
        url = "http://172.16.11.26:8001/api/v29+/auth?name=admin&password=123456"
        r = requests.get(url)
        import json
        j = {}
        j = json.loads(r.content)
        self.token = j["token"]

    def render_GET(self, request):
        request.setHeader(b"content-type", b"application/json")
        s.get_token()
        import requests
        broadcast_status_list = json.loads("{}")
        if self.token is not None:
            url = "http://172.16.11.26:8001/api/v29+/ws/forwarder"
            body = json.loads("{}")
            body["company"] = "BL"
            body["actioncode"] = "c2ls_get_server_terminals_status"
            body["token"] = self.token
            body["data"] = ""
            body["result"] = 200
            body["return_message"] = ""
            body["sign"] = "rand string"
            r1 = requests.put(url, data=body)
            j1 = None
            try:
                j1 = json.loads(r1.content)
            except json.JSONDecodeError:
                pass
            if j1 is not None:
                points = j1["data"]["EndPointsArray"]
                for point in points:
                    item = "BROADCAST" + str(point["EndpointID"])
                    broadcast_status_list[item] = {}
                    broadcast_status_list[item]["status"] = points["Status"]
        # 终端工作状态 0-离线,1-在线 2-占用
        return json.dumps(broadcast_status_list).encode("utf-8")

    def render_POST(self, request):
        request.setHeader(b"content-type", b"application/json")
        body = request.content.read()
        j = None
        try:
            j = json.loads(body)
        except json.JSONDecodeError:
            pass
        device = j["device"]
        tag = j["tag"]
        value = j["value"]

        return b"Hello, this is the control API."


root = Resource()
api = Resource()
# root.getChild(b"api", api).putChild(b"data", Data())
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

from apps import BroadcastProtocol, SendHelper

s = SendHelper(agent=agent, ip_port=ip_port)

reactor.listenTCP(metro_view_port, factory)
reactor.run()
