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

    def dataParse(self, data: bytes):
        """
        数据解析
        @param data:
        @return:
        """
        pass

    def heart_beat(self):
        """
        心跳
        @return:
        """
        pass

    @staticmethod
    def http_client(cls):
        """
        增加http client相关的变量与方法
        @param cls:
        @return:
        """
        cls.remote_host = None
        cls.remote_port = None
        return cls

    @staticmethod
    def interval(value: str):
        """
        用于间隔通信的装饰器
        @param value:
        @return:
        """
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
