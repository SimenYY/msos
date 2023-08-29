#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@FileName：deviceProtocol.py
@Description：设备协议基类以及相关功能项
@Author：SimenYY
@Time：2023/8/28 14:53
@Department：公路机电工程技术中心
@Copyright：©1999-2023 浙江中控信息产业股份有限公司
"""

from twisted.internet.protocol import Protocol
from twisted.internet import reactor

import time
from functools import wraps


class DeviceProtocol(Protocol):

    def dataReceived(self, data: bytes):
        reactor.callInThread(self.dataParse, data)

    def dataParse(self, data: bytes) -> None:
        """
        @param data:
        @return:
        """
        pass

    def heart_beat(self) -> None:
        pass

    @staticmethod
    def web_client(cls):
        cls.remote_host = None
        cls.remote_port = None
        return cls

    @staticmethod
    def interval(value: str):
        value = value.split('/')
        unit = value[1]
        if 'second' == unit:
            seconds = int(value[0])
        elif 'minute' == unit:
            seconds = 60 * int(value[0])
        elif 'hour' == unit:
            seconds = 3600 * int(value[0])

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                while True:
                    func(*args, **kwargs)
                    time.sleep(seconds)

            return wrapper

        return decorator
