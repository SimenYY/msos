#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@FileName：config.py
@Description：配置文件
@Author：SimenYY
@Time：2023/8/28 14:53
@Department：公路机电工程技术中心
@Copyright：©1999-2023 浙江中控信息产业股份有限公司
"""

from protocol import *

config = {
    'app': {
        'port': 28889,
        'ip': '0.0.0.0',
        'is_debug': False,
    },
    'log': {
        'level': 'info',
        'rotation': '00:00',
        'retention': '15 days'
    },
    'device_list': [
        {
            # 天线
            'device_name': 'Antenna',
            'protocol_type': 'HTTPS',
            'protocol_name': AntennaProtocol,
            'is_enable': False,
            'ip_list': [
                '127.0.0.1',
                # '172.20.61.125'
            ],
            'port': 5000
        },
        {
            # 永基节点机
            'device_name': 'smart',
            'protocol_type': 'TCP',
            'protocol_name': YoujiProtocol,
            'is_enable': True,
            'ip_list': [
                '127.0.0.1'
            ],
            'port': 31517
        }
    ]
}
