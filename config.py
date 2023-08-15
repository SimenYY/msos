# -*- coding: utf-8 -*-

config = {
    'app': {
        'port': 28889,
        'ip': '0.0.0.0',
        'is_debug': False
    },
    'factory_list': [
        {
            'device_name': 'broadcast',
            'protocol_type': 'TCP',
            'is_enable': True,
            'ip_list': [
                '127.0.0.1',
                '172.20.61.6'
            ],
            'port': 502
        },
        {
            'device_name': 'Phone',
            'protocol_type': 'TCP',
            'is_enable': False,
            'ip_list': [],
            'port': 0
        }
    ]
}
