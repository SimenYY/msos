#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@FileName：antennaProtocol.py
@Description：镜湖收费站天线接口
@Author：SimenYY
@Time：2023/8/24 17:30
@Department：公路机电工程技术中心
@Copyright：©1999-2023 浙江中控信息产业股份有限公司
"""

import base64
import requests
from loguru import logger
from twisted.internet import reactor

from data.value import value_dic
from protocol.deviceProtocol import DeviceProtocol


@DeviceProtocol.http_client
class AntennaProtocol(DeviceProtocol):
    """
    @projectName: 镜湖收费站
    @projectFile: https://alidocs.dingtalk.com/i/nodes/20eMKjyp81R7ePKGfwQ0w1xwWxAZB1Gv?utm_scene=person_space
    @protocolName: 镜湖收费站天线协议
    @description:
    """

    def __init__(self):
        # fixme: 如果在这里增加类成员初始化的话，会报错，buildProtocol中的self.protocol()会执行不下去
        reactor.callInThread(self.get_device_info)

    @DeviceProtocol.interval('1/second')
    def get_device_info(self):
        """
        功能：获取天线设备信息和状态信息
        :return: None
        """
        url = []
        if self.remote_host == '127.0.0.1' or '172.20.61.125':
            url.append('http://')
            url.append(f'{self.remote_host}:{self.remote_port}')
            url.append('/cgi-bin/rsuinfo')
            url = ''.join(url)
        else:
            url.append('https://')
            url.append(self.remote_host)
            url.append('/cgi-bin/rsuinfo')
            url = ''.join(url)

        try:
            ret = requests.get(url)
        except requests.exceptions.ConnectionError:
            logger.error(f'ConnectionError, url={url}')
        else:
            encoded_ret = base64.b64decode(ret.content).decode('GB2312')
            import json
            json_ret = json.loads(encoded_ret)
            antenna = {}
            antenna['device_type'] = json_ret.get('device_type', "")
            antenna['power_up_time'] = json_ret.get('power_up_time', 0)
            antenna['ip'] = json_ret.get('ip', "")
            antenna['rsu_id'] = json_ret.get('rsu_id', "")
            antenna['power'] = json_ret.get('power', 0)
            antenna['wait_time'] = json_ret.get('wait_time', 0)
            antenna['antenna_area'] = json_ret.get('antenna_area', "")
            antenna['control_temperature'] = json_ret.get('control_temperature', 0)
            antenna['antenna_temperature'] = json_ret.get('antenna_temperature', 0)
            # 异常
            exceptions = json_ret.get('exception', [])
            str_list = []
            str_list.append('[')
            for exception in exceptions:
                str_list.append('{')
                str_list.append('"explain":"')
                str_list.append(exception.get('explain'))
                str_list.append('",')
                str_list.append('"err_code":')
                str_list.append(str(exception.get('err_code')))
                str_list.append('}')
                str_list.append(',')
            str_list.pop()
            str_list.append(']')
            antenna['exception'] = ''.join(str_list)
            # 交易成功率信息
            rate_list = json_ret.get('trade_success_rate', [])
            str_list = []
            for rate in rate_list:
                str_list.append(rate)
            antenna['trade_success_rate'] = str(str_list)
            status_list = json_ret.get('psam_status', [])
            str_list = []
            for status in status_list:
                str_list.append(status)
            antenna['psam_status'] = str(str_list)

            value_dic['antenna'] = antenna

            logger.info(encoded_ret)
