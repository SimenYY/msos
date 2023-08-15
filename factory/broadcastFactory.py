# -*- coding: utf-8 -*-

from twisted.internet.protocol import ReconnectingClientFactory

from factory.deviceFactory import DeviceFactory
from protocol import *


class BroadcastFactory(DeviceFactory, ReconnectingClientFactory):
    protocol = BroadcastProtocol
