# -*- coding: utf-8 -*-

from flask import Flask
from flask_twisted import Twisted
from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory

from data.value import value_dic

app = Flask(__name__)
twisted = Twisted(app)


@app.route('/api/data', methods=['GET'])
def api_data():
    return value_dic


@app.route('/api/control', methods=['POST'])
def api_control():
    pass


def main():
    from config import config
    from factory.deviceFactory import DeviceFactory
    factory_list = config['factory_list']
    for factory in factory_list:
        if factory['is_enable']:
            # 通过反射返回继承了设备工厂的子工厂
            device_name = factory['device_name'].lower().capitalize()
            f = DeviceFactory.buildSubFactory(device_name)
            ip_list = factory['ip_list']
            protocol_type = factory['protocol_type']
            port = factory['port']
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
