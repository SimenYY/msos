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
from protocol.deviceProtocol import DeviceProtocol, web_client, Interval

logger.add('..\logs\log_antenna.log')


@web_client
class AntennaProtocol(DeviceProtocol):

    """
    @项目名称：镜湖收费站
    @项目协议：https://alidocs.dingtalk.com/i/nodes/20eMKjyp81R7ePKGfwQ0w1xwWxAZB1Gv?utm_scene=person_space
    """

    def __init__(self):
        reactor.callInThread(self.get_device_info)

    @Interval('1/second')
    def get_device_info(self):
        """
        功能：获取天线设备信息和状态信息
        :return:
        """
        url = []
        url.append('https://')
        url.append(self.remote_host)
        url.append('/cgi-bin/rsuinfo')
        url = ''.join(url)
        try:
            ret = requests.get(url)
        except requests.exceptions.ConnectionError:
            logger.error('ConnectionError')
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
            # todo 待确认
            antenna['exception'] = json_ret.get('exception', [])
            # todo 待确认
            antenna['trade_success_rate'] = json_ret.get('trade_success_rate', [])
            # todo 待确认
            antenna['psam_status'] = json_ret.get('psam_status', [])

            value_dic['antenna'] = antenna

            logger.info(encoded_ret)

    # @Interval('1/second')
    # def test(self):
    #     url = []
    #     url.append('http://')
    #     url.append(self.remote_host)
    #     url.append(':')
    #     url.append(str(self.remote_port))
    #     url.append('/test')
    #     url = ''.join(url)
    #     try:
    #         ret = requests.get(url)
    #         value_dic['test'] = ret.content.decode('utf-8')
    #     except requests.exceptions.ConnectionError:
    #         print("ConnectionError")
    #     import datetime
    #     print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
