from twisted.internet import reactor
from device.vehicle.apps import VehicleClientFactory

host = 'localhost'
port = 8000
port = 8001
if __name__ == "__main__":
    f = VehicleClientFactory()
    f1 = VehicleClientFactory()
    reactor.connectTCP(host, port, f)
    reactor.connectTCP(host, port, f1)
    reactor.run()
