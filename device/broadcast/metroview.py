from twisted.internet import reactor
from twisted.web.client import HTTPConnectionPool, Agent
from twisted.web.server import Site
from twisted.web.resource import Resource


class Drive(Resource):
    def render_GET(self, request):
        request.setHeader(b"content-type", b"application/json")
        return b"Hello, this is the data API."

    def render_POST(self, request):
        request.setHeader(b"content-type", b"application/json")
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
metro_view_port = config["metroview"]["port"]
ip_port = config["apps"]["ip_port"]

from apps import BroadcastProtocol, SendHelper

s = SendHelper(agent=agent, ip_port=ip_port)
s.get_token()

reactor.listenTCP(metro_view_port, factory)
reactor.run()
