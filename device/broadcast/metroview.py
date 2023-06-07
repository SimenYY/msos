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
        self.init_time = datetime.datetime.now()

    def render_GET(self, request):
        request.setHeader(b"content-type", b"application/json")

        # 超过1h，刷新一下token
        current_time = datetime.datetime.now()
        time_diff = current_time - self.init_time
        if time_diff.total_seconds() > 3600:
            self.token = base_req.refresh_token(self.token)
        id_status = base_req.get_terminal_status(self.token)

        return json.dumps(id_status).encode("utf-8")

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
