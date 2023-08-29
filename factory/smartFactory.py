#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@FileName：smartFactory.py
@Description：节点机设备类
@Author：SimenYY
@Time：2023/8/28 14:53
@Department：公路机电工程技术中心
@Copyright：©1999-2023 浙江中控信息产业股份有限公司
"""

from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol
from typing import Optional

from factory.deviceFactory import DeviceFactory


class SmartFactory(DeviceFactory):
    instances = []
