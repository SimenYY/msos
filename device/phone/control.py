from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.web.client import HTTPConnectionPool, Agent
from twisted.web.server import Site
from twisted.web.resource import Resource
from apps import ExternalPhone
import datetime
from core import core_endpoint_status

class Drive(Resource):

    def __init__(self):
        super().__init__()
        self.init_time = datetime.datetime.now()

    def render_GET(self, request):
        request.setHeader(b"content-type", b"application/json")

        ret = p.get_endpoint_list()
        if ret["code"] == 200:
            return core_endpoint_status(ret).encode('utf-8')
        else:
            return ret.encode('utf-8')
    def render_POST(self, request):
        pass


root = Resource()
api = Resource()
# root.getChild(b"api", api).putChild(b"data", Data())
root.putChild(b"api", api)
api.putChild(b"data", Drive())
api.putChild(b"control", Drive())
factory = Site(root)

pool = HTTPConnectionPool(reactor)
agent = Agent(reactor, pool=pool)

with open('./phone.json', 'r') as c:
    import json

    config = json.load(c)
metro_view_port = config["metro_view"]["port"]
addr = config["apps"]["address"]
p = ExternalPhone("admin:admin246", addr)



reactor.listenTCP(metro_view_port, factory)
reactor.run()
