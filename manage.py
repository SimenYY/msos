from twisted.internet import reactor
from twisted.python import log
from twisted.internet.task import LoopingCall
from device.vd.apps import VehicleClientFactory
from device.vms.apps import VMSClientFactory
from device.phone.apps import PhoneClientFactory

import sys


def init():
    # 初始化线程池线程数量
    reactor.suggestThreadPoolSize(30)

    # 利用字典调用函数
    factory_dic = {
        'VMSClientFactory': VMSClientFactory,
        'VehicleClientFactory': VehicleClientFactory,
        'PhoneClientFactory': PhoneClientFactory
    }
    # 加载使能的驱动，并建立连接
    with open('./config.json', 'r') as c:
        import json
        config = json.load(c)
    device = config['device']
    for key, value in device.items():
        if value['enable'] == 1:
            fun_str = key + "ClientFactory"
            reactor.connectTCP(value['ip'], value['port'], factory_dic[fun_str]())


def run():
    reactor.run()


def test():
    print(1)


if __name__ == "__main__":
    init()
    run()
