# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_twisted import Twisted
from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory

from data.value import value_dic

from loguru import logger

app = Flask(__name__)
twisted = Twisted(app)

# 接口列表
instance_list = {}


@app.route('/api/data', methods=['GET'])
def api_data():
    return value_dic


@app.route('/api/control', methods=['POST'])
def api_control():
    try:
        device_list = request.get_json()
    except ValueError as e:
        logger.error('The request data is not in JSON format: {}', e)
        ret = {}
        ret['data'] = {}
        ret['data']['message'] = 'ValueError'
        ret['data']['resultCode'] = 0
        ret['status'] = 'error'
        return ret

    device_code_list = []
    for device in device_list:
        device_code = device.get('deviceCode')
        if device_code is not None:
            device_code_list.append(device_code)
    content = device.get('content')
    # 拆分成‘对象’+‘逻辑’，然后作为入参
    if not device_code_list and content is not None:
        #todo 回调设备类的处理函数
        pass



def main():
    from factory.deviceFactory import DeviceFactory
    from config import config
    device_list = config['device_list']
    for device in device_list:
        if device['is_enable']:
            device_name = device['device_name'].lower().capitalize()
            # 构建设备类
            f = DeviceFactory.buildSubFactory(device_name)
            # 建立对应表
            instance_list[device_name] = f
            ip_list = device['ip_list']
            protocol_type = device['protocol_type']
            port = device['port']
            if 'TCP' == protocol_type:
                bases = []
                bases.append(ReconnectingClientFactory)
                # 动态混入
                f.__bases__ += tuple(bases)
                for ip in ip_list:
                    reactor.connectTCP(ip, port, f())
            elif 'HTTP' == protocol_type:
                pass
            elif 'UDP' == protocol_type:
                pass

    ip = config['app'].get('ip', '0.0.0.0')
    port = config['app'].get('port', 28889)
    debug = config['app'].get('is_debug', False)

    twisted.run(ip=ip, port=port, debug=debug)


if __name__ == '__main__':
    main()
