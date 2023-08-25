# -*- coding: utf-8 -*-
from twisted.internet.protocol import Factory
from factory import *


class DeviceFactory(Factory):
    """
    设备工厂抽象类，用于项目适配的自定义工厂类, 默认继承原始Factory，后续扩展可动态继承父类
    """

    def __init__(self, protocol):
        self.protocol = protocol

    @classmethod
    def buildSubFactory(cls, assembly_name):
        """
        通过反射技术根据字符串构造响应的子类工程
        :param assembly_name:
        :return:
        """
        factory_name = ''.join([assembly_name, 'Factory'])
        dic = {}
        for sub in DeviceFactory.__subclasses__():
            dic[sub.__name__] = sub
        if factory_name in dic.keys():
            return dic[factory_name]
        else:
            return None
