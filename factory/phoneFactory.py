# -*- coding: utf-8 -*-
from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol
from typing import Optional

from factory.deviceFactory import DeviceFactory
from protocol import *


class PhoneFactory(DeviceFactory):
    protocol = PhoneProtocol
    instances = []

    def buildProtocol(self, addr: IAddress) -> "Optional[Protocol]":
        p = self.protocol()
        p.factory = self
        self.instances.append(p)
        self.protocol.remote_host = addr.host
        self.protocol.remote_port = addr.port
        return p
