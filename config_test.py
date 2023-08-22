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
            'port_list': [
                8000,
                8001,
                8002,
                8003
            ],
            'ip': '127.0.0.1'
        },
    ]
}
