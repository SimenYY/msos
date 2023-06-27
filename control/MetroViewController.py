# coding = utf-8
from twisted.web.resource import Resource
import json
from core.broadcastCoreServicer import BroadcastCoreServicer


class MetroViewController(Resource):
    def __int__(self):
        pass

    def render_GET(self, request):
        request.setHeader(b"content-type", b"application/json")

    def render_POST(self, request):
        request.setHeader(b"content-type", b"application/json")

        body = request.content.read()
        devices = None
        try:
            devices = json.loads(body)
        except json.JSONDecodeError:
            return b"JSON format is invalid!"

        b = BroadcastCoreServicer(devices)

        return b"b"