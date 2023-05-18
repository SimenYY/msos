from twisted.internet import reactor
from twisted.python import log

from device.vehicle.apps import VehicleClientFactory
from device.vms.apps import VMSClientFactory
from device.phone.apps import PhoneClientFactory


import sys

if __name__ == "__main__":
    log.startLogging(sys.stdout)
    # reactor.connectTCP('localhost', 8000, VehicleClientFactory())
    # reactor.connectTCP('localhost', 9000, VMSClientFactory())
    reactor.connectTCP('localhost', 9001, PhoneClientFactory("ws://127.0.0.1:9001"))
    reactor.run()
