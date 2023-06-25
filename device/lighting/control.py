from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.web.client import HTTPConnectionPool, Agent
from twisted.web.server import Site
from twisted.web.resource import Resource
from apps import LightingClientFactory
import datetime
import json

class Drive(Resource):

    def __init__(self):
        super().__init__()
        self.init_time = datetime.datetime.now()
    def render_GET(self, request):
        request.setHeader(b"content-type", b"application/json")
        ret = light.protocol.status_list
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

light = LightingClientFactory()
reactor.connectTCP("172.16.11.19", 1001, light)
reactor.listenTCP(28892, factory)
reactor.run()
