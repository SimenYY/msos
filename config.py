# -*- coding: utf-8 -*-
from protocol import *

config = {
    'app': {
        'port': 28889,
        'ip': '0.0.0.0',
        'is_debug': False
    },
    'device_list': [
        {
            'device_name': 'broadcast',
            'protocol_type': 'TCP',
            'is_enable': False,
            'ip_list': [
                '127.0.0.1',
            ],
            'port': 502
        },
        {
            'device_name': 'Phone',
            'protocol_type': 'HTTP',
            'is_enable': False,
            'ip_list': [
                '127.0.0.1'
            ],
            'port': 5500
        },
        {
            'device_name': 'Antenna',
            'protocol_type': 'HTTP',
            'protocol_name': AntennaProtocol,
            'is_enable': True,
            'ip_list': [
                '127.0.0.1'
            ],
            'port': 5000
        }
    ]
}
