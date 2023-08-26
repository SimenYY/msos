from typing import Optional

from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol

from factory.deviceFactory import DeviceFactory


class VmsFactory(DeviceFactory):
    instances = []

    def buildProtocol(self, addr: IAddress) -> "Optional[Protocol]":
        p = self.protocol()
        p.factory = self
        self.instances.append(p)
        return p

