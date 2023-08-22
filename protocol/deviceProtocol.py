# -*- coding: utf-8 -*-

from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet import reactor

import time
from functools import wraps


class DeviceProtocol(Protocol):

    def dataReceived(self, data: bytes):
        reactor.callInThread(self.dataParse, data)

    def dataParse(self, data: bytes):
        """
        负责目标数据的解析工作
        :param data:
        :return:
        """
        pass


class Interval:
    """
    用类的形式定义的通信间隔装饰器，参数输入标准参照方便用户观察的形式，
    例如‘1/second、3/minute、5/hour’的形式来定义
    """

    def __init__(self, value: str):
        value = value.split('/')
        unit = value[1]
        if 'second' == unit:
            self.seconds = int(value[0])
        elif 'minute' == unit:
            self.seconds = 60 * int(value[0])
        elif 'hour' == unit:
            self.seconds = 3600 * int(value[0])

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                func(*args, **kwargs)
                time.sleep(self.seconds)

        return wrapper

