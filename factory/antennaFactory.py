#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@FileName：antennaFactory.py
@Description：天线接口设备类
@Author：SimenYY
@Time：2023/8/28 14:53
@Department：公路机电工程技术中心
@Copyright：©1999-2023 浙江中控信息产业股份有限公司
"""

from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol
from typing import Optional

from factory.deviceFactory import DeviceFactory


class AntennaFactory(DeviceFactory):
    instances = []

    def buildProtocol(self, addr: IAddress) -> "Optional[Protocol]":
        self.protocol.remote_host = addr.host
        self.protocol.remote_port = addr.port
        return super().buildProtocol(addr)




