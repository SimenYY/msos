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
        request.setHeader(b"content-type", b"application/json")
        body = request.content.read()
        devices = None
        try:
            devices = json.loads(body)
        except json.JSONDecodeError:
            pass
        if devices is not None:
            for device in devices:
                if device['content']['action'] == 'mode_ctrl':
                    value = device['content']['mode']
                    mode = value.to_bytes(1, byteorder='big', signed=False)
                    msg = b'\x00\x00\x00\x00\x00\x09\x01\x10' \
                          b'\x03\xE9\x00\x01\x02\x00' + mode
                    light.protocol.transport.write(msg)
                    return b'send' + msg
                    break
                elif device['content']['action'] == 'brightness_ctrl':
                    brightness = device['content']['brightness']
                    brightness_16 = brightness.to_bytes(1, byteorder='big')
                    id_ = device['deviceCode'][9:]
                    addr_10 = 1200 + 2 * int(id_) - 1
                    addr_16 = addr_10.to_bytes(2, byteorder='big')

                    msg = b'\x00\x00\x00\x00\x00\x0B\x01' \
                          b'\x10' + addr_16 + b'\x00\x02' \
                          b'\x04\xFF' + brightness_16 + b'\xFF\xFF'
                    light.protocol.transport.write(msg)
                    return b'send' + msg

root = Resource()
api = Resource()
root.putChild(b"api", api)
api.putChild(b"data", Drive())
api.putChild(b"control", Drive())
factory = Site(root)

pool = HTTPConnectionPool(reactor)
agent = Agent(reactor, pool=pool)

light = LightingClientFactory()
#ip = "172.16.11.19"
ip = '127.0.0.1'
reactor.connectTCP(ip, 1001, light)
reactor.listenTCP(28892, factory)
reactor.run()
