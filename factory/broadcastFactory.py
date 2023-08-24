# -*- coding: utf-8 -*-
from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol
from typing import Optional

from factory.deviceFactory import DeviceFactory
from protocol import *


class BroadcastFactory(DeviceFactory):
    instances = []

