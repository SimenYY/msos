#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@FileName：deviceFactory.py
@Description：设备类基类
@Author：SimenYY
@Time：2023/8/28 14:53
@Department：公路机电工程技术中心
@Copyright：©1999-2023 浙江中控信息产业股份有限公司
"""

from typing import Optional

from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Factory, Protocol

from factory import *


class DeviceFactory(Factory):
    instances = None

    def __init__(self, protocol):
        self.protocol = protocol

    def buildProtocol(self, addr: IAddress) -> "Optional[Protocol]":
        p = self.protocol()
        p.factory = self
        self.instances.append(p)
        return p

    @classmethod
    def buildSubFactory(cls, assembly_name: str):
        """
        通过反射技术根据字符串构造响应的子类工程
        :param assembly_name: 设备名字符串
        :return: None or class
        """
        factory_name = ''.join([assembly_name, 'Factory'])
        dic = {}
        for sub in DeviceFactory.__subclasses__():
            dic[sub.__name__] = sub
        if factory_name in dic.keys():
            return dic[factory_name]
        else:
            return None
