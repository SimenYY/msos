# -*- coding: utf-8 -*-
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
            'device_name': 'Antenna',
            'protocol_type': 'HTTPS',
            'protocol_name': AntennaProtocol,
            'is_enable': True,
            'ip_list': [
                '127.0.0.1'
            ],
            'port': 5000
        },
        {
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
