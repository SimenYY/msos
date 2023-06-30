from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.web.client import HTTPConnectionPool, Agent
from twisted.web.server import Site
from twisted.web.resource import Resource
from apps import VehicleClientFactory, VehicleProtocol
import datetime


class Drive(Resource):

    def __init__(self):
        super().__init__()
        self.init_time = datetime.datetime.now()

    def render_GET(self, request):
        request.setHeader(b"content-type", b"application/json")

        ret = {}
        for vd in vd_list:
            k = ''.join(["VD", str(vd_list.index(vd) + 1)])
            ret[k] = vd.protocol.vd_msg

        return json.dumps(ret).encode('utf-8')

    def render_POST(self, request):
        pass


root = Resource()
api = Resource()
root.putChild(b"api", api)
api.putChild(b"data", Drive())
api.putChild(b"control", Drive())
factory = Site(root)

pool = HTTPConnectionPool(reactor)
agent = Agent(reactor, pool=pool)

with open('./vd.json', 'r') as c:
    import json

    config = json.load(c)
metro_view_port = config["metro_view"]["port"]

ip_list = [
    "192.168.22.51",
    "192.168.22.52",
    "192.168.22.53",
    "192.168.22.54",
    "192.168.22.55",
    "192.168.22.56",
    "192.168.22.57",
    "192.168.22.58",
]
vd_list = []
for ip in ip_list:
    vd = VehicleClientFactory()
    vd_list.append(vd)
    reactor.connectTCP(ip, 20001, vd)

reactor.listenTCP(metro_view_port, factory)
reactor.run()
