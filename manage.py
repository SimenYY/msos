from twisted.internet import reactor
from twisted.python import log

from device.vehicle.apps import VehicleClientFactory
from device.vms.apps import VMSClientFactory
from device.phone.apps import PhoneClientFactory

import sys

if __name__ == "__main__":
    reactor.suggestThreadPoolSize(3)
    log.startLogging(sys.stdout)
    reactor.connectTCP('localhost', 8000, VehicleClientFactory())
    reactor.connectTCP('localhost', 9000, VMSClientFactory())
    reactor.connectTCP('localhost', 9001, PhoneClientFactory())
    reactor.run()
