from twisted.internet import reactor
from twisted.web.server import Request, Site
from twisted.web.resource import Resource
import json


class AdvCore(Resource):
    def render_GET(self, request):
        # request.setHeader("Content-Type", "application/json")
        if request.path == "/cmd/":
            print(1)
        elif request.path == "/inquire/":
            print(2)


root = AdvCore()
root.putChild(b"advcore", AdvCore())
factory = Site(root)
reactor.listenTCP(8080, factory)
reactor.run()




