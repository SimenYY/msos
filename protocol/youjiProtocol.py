#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@FileName：youjiProtocol.py
@Description：
@Author：SimenYY
@Time：2023/8/28 14:53
@Department：公路机电工程技术中心
@Copyright：©1999-2023 浙江中控信息产业股份有限公司
"""

import json

from loguru import logger
from twisted.internet.protocol import connectionDone
from twisted.internet import reactor
from twisted.python import failure

from protocol.deviceProtocol import DeviceProtocol
from data.value import value_dic


class YoujiProtocol(DeviceProtocol):
    def connectionMade(self):
        logger.info(f'连接到主机:{self.transport.getPeer().host} {self.transport.getPeer().port}')
        self.login_ack()
        reactor.callInThread(self.heart_beat)
        # self.query_all_device_data()

    def dataReceived(self, data: bytes):
        logger.info(f'收到数据来自{self.transport.getPeer().host}:{data}')
        super().dataReceived(data)

    def connectionLost(self, reason: failure.Failure = connectionDone):
        logger.error(reason)

    def dataParse(self, data: bytes):
        str_data = data.decode('GB18030')
        smart = {}
        str_data = str_data[:-1]
        try:
            j = json.loads(str_data)
        except ValueError as e:
            logger.error(f"数据不满足JSON格式:{e}")
            return
        else:
            MSG = j.get('MSG')
            if MSG != 64:
                return
            rt_spm = j.get('rt_spm')

            # 有线主网配置
            rj_45 = rt_spm.get('rj45')
            for k, v in rj_45.items():
                smart[''.join(['rj45_', k])] = v
            # 有线主网状态
            rt_rj45 = rt_spm.get('rt_rj45')
            for k, v in rt_rj45.items():
                smart[''.join(['rt_rj45_', k])] = v
            # 有线备网配置
            rj45r = rt_spm.get('rj45r')
            for k, v in rj45r.items():
                smart[''.join(['rj45r_', k])] = v
            # 有线备网状态
            rt_rj45r = rt_spm.get('rt_rj45r')
            for k, v in rt_rj45r.items():
                smart[''.join(['rt_rj45r_', k])] = v
            # 供电状态
            rt_power = rt_spm.get('rt_power')
            for k, v in rt_power.items():
                smart[''.join(['rt_power_', k])] = v
            # 外接设备
            owners = rt_spm.get('owners')
            for owner in owners:
                name = owner.get('name')
                if '节点机' == name:
                    device_name = 'JieDianJi'
                elif '栏杆机' == name:
                    device_name = 'LanGanJi'
                elif '前抓拍相机' == name:
                    device_name = 'QianZhuaPaiXiangJi'
                elif '折叠屏' == name:
                    device_name = 'ZheDiePing'

                binds = owner.get('binds')
                for bind in binds:
                    values = bind.get('values')
                    for value in values:
                        value_name = value.get('name')
                        v = value.get('value')
                        num_type = v[:1]
                        num = v[1:]
                        if 'b' == num_type:
                            v = bool(num)
                        elif 'i' == num_type:
                            v = int(num)
                        elif 'f' == num_type:
                            v = float(num)
                        smart[''.join([device_name, '_', value_name])] = v

            value_dic['smart_' + self.transport.getPeer().host] = smart

    def login_ack(self):
        j = {}
        j['MSG'] = 6
        j['ack'] = 3
        j['type'] = 2
        j['flag'] = 0
        import time
        j['time'] = int(time.time())
        str = json.dumps(j) + '\0'
        self.transport.write(str.encode('GB18030'))
        logger.info(f'发送数据到往{self.transport.getPeer().host}:{str.encode("GB18030")}')

    @DeviceProtocol.interval('3/second')
    def heart_beat(self):
        j = {}
        j['MSG'] = 0
        j['alive'] = 0
        import time
        j['time'] = int(time.time())
        str = json.dumps(j) + '\0'
        self.transport.write(str.encode('GB18030'))
        logger.info(f'发送数据到往{self.transport.getPeer().host}:{str.encode("GB18030")}')

    def query_all_device_data(self):
        j = {}
        j['MSG'] = 160
        j['oid'] = 0
        j['sdm'] = '192.168.3.24'
        j['owners'] = None
        str = json.dumps(j) + '\0'
        self.transport.write(str.encode('GB18030'))
        logger.info(f'发送数据到往{self.transport.getPeer().host}:{str.encode("GB18030")}')
