# -*- coding: utf-8 -*-
from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol
from typing import Optional

from factory.deviceFactory import DeviceFactory


class SmartFactory(DeviceFactory):
    instances = []

    def buildProtocol(self, addr: IAddress) -> "Optional[Protocol]":
        p = self.protocol()
        p.factory = self
        self.instances.append(p)
        return p

