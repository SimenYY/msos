# -*- coding: utf-8 -*-
import time

from flask import Flask, request
from flask_twisted import Twisted
from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory

from data.value import value_dic

from loguru import logger

app = Flask(__name__)
twisted = Twisted(app)

# 设备名与对应工厂类
class_list = {}


@app.route('/api/data', methods=['GET'])
def api_data():
    return value_dic


@app.route('/api/control', methods=['POST'])
def api_control():
    ret = {}
    ret['data'] = {}
    # json格式校验
    try:
        device_list = request.get_json()
    except ValueError as e:
        logger.error('The request data is not in JSON format: {}', e)
        ret['data']['message'] = 'ValueError'
        ret['data']['resultCode'] = 1
        ret['status'] = 'error'
        return ret

    # 建立device_code_list和提取content
    device_code_list = []
    for device in device_list:
        device_code = device.get('deviceCode')
        if device_code is not None:
            device_code_list.append(device_code)
    content = device.get('content')

    # 拆分成‘对象’+‘逻辑’，然后作为该设备类的执行函数的入参
    if device_code_list and content:
        device_name = device_code_list[0].split('_')[0].lower().capitalize()
        f = class_list[device_name]
        for instance in f.instances:
            # todo 异步执行设备控制动作，或者考虑多线程
            instance.execute(device_code_list, content)
    else:
        logger.error('Incorrect json parameter')
        ret['data']['message'] = 'Incorrect json parameter'
        ret['data']['resultCode'] = 1
        ret['status'] = 'error'
        return ret

    ret['data']['message'] = 'Control success'
    ret['data']['resultCode'] = 0
    ret['status'] = 'success'
    return ret


def main():
    from factory.deviceFactory import DeviceFactory
    from config import config
    device_list = config['device_list']

    for device in device_list:
        if device['is_enable']:

            # 设备名大小写不敏感
            device_name = device['device_name'].lower().capitalize()
            protocol_name = device['protocol_name']
            protocol_type = device['protocol_type']
            port = device['port']
            ip_list = device['ip_list']

            # 构建设备类
            f = DeviceFactory.buildSubFactory(device_name)
            # 建立”设备名-设备工厂类“对应表
            class_list[device_name] = f

            if 'TCP' == protocol_type:
                bases = []
                bases.append(ReconnectingClientFactory)
                # 动态混入
                f.__bases__ += tuple(bases)

                for ip in ip_list:
                    reactor.connectTCP(ip, port, f(protocol_name))

            elif 'HTTP' == protocol_type:
                # 初始化web远程ip和port
                factory_instance = f(protocol_name)
                from twisted.internet.address import IPv4Address
                factory_instance.buildProtocol(IPv4Address(
                    type='TCP',
                    host=device['ip_list'][0],
                    port=device['port']
                ))

            elif 'UDP' == protocol_type:
                pass

    ip = config['app'].get('ip', '0.0.0.0')
    port = config['app'].get('port', 28889)
    debug = config['app'].get('is_debug', False)

    twisted.run(ip=ip, port=port, debug=debug)


if __name__ == '__main__':
    main()
