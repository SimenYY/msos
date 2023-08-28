# -*- coding: utf-8 -*-
import json

from loguru import logger
from twisted.internet.protocol import connectionDone
from twisted.internet import reactor
from twisted.python import failure

from protocol.deviceProtocol import DeviceProtocol, Interval

from data.value import value_dic


class YoujiProtocol(DeviceProtocol):
    def connectionMade(self):
        logger.info(f'连接到主机:{self.transport.getPeer().host} {self.transport.getPeer().port}')
        self.login_ack()
        reactor.callInThread(self.heart_beat)
        #self.query_all_device_data()

    def dataReceived(self, data: bytes):
        logger.info(f'收到数据来自{self.transport.getPeer().host}:{data}')
        super().dataReceived(data)

    def connectionLost(self, reason: failure.Failure = connectionDone):
        logger.error(reason)

    def dataParse(self, data: bytes):
        str = data.decode('GB18030')
        str = str[:-1]
        try:
            j = json.loads(str)
        except ValueError as e:
            logger.error(f"数据不满足JSON格式:{e}")
            return
        else:
            MSG = j.get('MSG')
            if MSG != 64:
                return
            rt_spm = j.get('rt_spm')

            # 有线主网配置
            rj45_sig = rt_spm.get('rj45').get('sig')
            rj45_dhcp = rt_spm.get('rj45').get('dhcp')
            rj45_ip = rt_spm.get('rj45').get('ip')
            rj45_sub = rt_spm.get('rj45').get('sub')
            rj45_gw = rt_spm.get('rj45').get('gw')
            rj45_dns = rt_spm.get('rj45').get('dns')
            rj45_ibdn = rt_spm.get('rj45').get('ibdn')
            rj45_server = rt_spm.get('rj45').get('server')
            rj45_port = rt_spm.get('rj45').get('port')
            rj45_hosts = rt_spm.get('rj45').get('hosts')
            rj45_ips = rt_spm.get('rj45').get('ips')
            # 有线主网状态
            rt_rj45_step = rt_spm.get('rt_rj45').get('step')
            rt_rj45_ip = rt_spm.get('rt_rj45').get('ip')
            rt_rj45_close = rt_spm.get('rt_rj45').get('close')
            rt_rj45_state = rt_spm.get('rt_rj45').get('state')
            rt_rj45_server = rt_spm.get('rt_rj45').get('server')
            rt_rj45_port = rt_spm.get('rt_rj45').get('port')
            rt_rj45_hosts = rt_spm.get('rt_rj45').get('hosts')
            rt_rj45_mac = rt_spm.get('rt_rj45').get('mac')
            # 有线备网配置
            rj45r_sig = rt_spm.get('rj45r').get('sig')
            rj45r_dhcp = rt_spm.get('rj45r').get('dhcp')
            rj45r_ip = rt_spm.get('rj45r').get('ip')
            rj45r_sub = rt_spm.get('rj45r').get('sub')
            rj45r_gw = rt_spm.get('rj45r').get('gw')
            rj45r_dns = rt_spm.get('rj45r').get('dns')
            rj45r_ibdn = rt_spm.get('rj45r').get('ibdn')
            rj45r_server = rt_spm.get('rj45r').get('server')
            rj45r_port = rt_spm.get('rj45r').get('port')
            rj45r_hosts = rt_spm.get('rj45r').get('hosts')
            rj45r_ips = rt_spm.get('rj45r').get('ips')
            # 有线备网状态
            rt_rj45r_step = rt_spm.get('rt_rj45r').get('step')
            rt_rj45r_ip = rt_spm.get('rt_rj45r').get('ip')
            rt_rj45r_close = rt_spm.get('rt_rj45r').get('close')
            rt_rj45r_state = rt_spm.get('rt_rj45r').get('state')
            rt_rj45r_server = rt_spm.get('rt_rj45r').get('server')
            rt_rj45r_port = rt_spm.get('rt_rj45r').get('port')
            rt_rj45r_hosts = rt_spm.get('rt_rj45r').get('hosts')
            rt_rj45r_mac = rt_spm.get('rt_rj45r').get('mac')
            # 供电状态
            rt_power_ac = rt_spm.get('rt_power').get('ac')
            rt_power_dc = rt_spm.get('rt_power').get('dc')
            rt_power_by = rt_spm.get('rt_power').get('by')
            rt_power_bat = rt_spm.get('rt_power').get('bat')
            rt_power_bav = rt_spm.get('rt_power').get('bav')
            rt_power_bai = rt_spm.get('rt_power').get('bai')
            rt_power_volac = rt_spm.get('rt_power').get('volac')
            rt_power_volups = rt_spm.get('rt_power').get('volups')

            smart = {}
            smart['rj45_sig'] = rj45_sig
            smart['rj45_dhcp'] = rj45_dhcp
            smart['rj45_ip'] = rj45_ip
            smart['rj45_sub'] = rj45_sub
            smart['rj45_gw'] = rj45_gw
            smart['rj45_dns'] = rj45_dns
            smart['rj45_ibdn'] = rj45_ibdn
            smart['rj45_server'] = rj45_server
            smart['rj45_port'] = rj45_port
            smart['rj45_hosts'] = rj45_hosts
            smart['rj45_ips'] = rj45_ips
            smart['rt_rj45_step'] = rt_rj45_step
            smart['rt_rj45_ip'] = rt_rj45_ip
            smart['rt_rj45_close'] = rt_rj45_close
            smart['rt_rj45_state'] = rt_rj45_state
            smart['rt_rj45_server'] = rt_rj45_server
            smart['rt_rj45_port'] = rt_rj45_port
            smart['rt_rj45_hosts'] = rt_rj45_hosts
            smart['rt_rj45_mac'] = rt_rj45_mac
            smart['rj45r_sig'] = rj45r_sig
            smart['rj45r_dhcp'] = rj45r_dhcp
            smart['rj45r_ip'] = rj45r_ip
            smart['rj45r_sub'] = rj45r_sub
            smart['rj45r_gw'] = rj45r_gw
            smart['rj45r_dns'] = rj45r_dns
            smart['rj45r_ibdn'] = rj45r_ibdn
            smart['rj45r_server'] = rj45r_server
            smart['rj45r_port'] = rj45r_port
            smart['rj45r_hosts'] = rj45r_hosts
            smart['rj45r_ips'] = rj45r_ips
            smart['rt_rj45r_step'] = rt_rj45r_step
            smart['rt_rj45r_ip'] = rt_rj45r_ip
            smart['rt_rj45r_close'] = rt_rj45r_close
            smart['rt_rj45r_state'] = rt_rj45r_state
            smart['rt_rj45r_server'] = rt_rj45r_server
            smart['rt_rj45r_port'] = rt_rj45r_port
            smart['rt_rj45r_hosts'] = rt_rj45r_hosts
            smart['rt_rj45r_mac'] = rt_rj45r_mac
            smart['rt_power_ac'] = rt_power_ac
            smart['rt_power_dc'] = rt_power_dc
            smart['rt_power_by'] = rt_power_by
            smart['rt_power_bat'] = rt_power_bat
            smart['rt_power_bav'] = rt_power_bav
            smart['rt_power_bai'] = rt_power_bai
            smart['rt_power_volac'] = rt_power_volac
            smart['rt_power_volups'] = rt_power_volups

            value_dic['smart_' + self.transport.getPeer().host] = smart

    def login_ack(self):
        j = {}
        j['MSG'] = 6
        j['ack'] = 3
        j['type'] = 2
        j['flag'] = 0
        import time
        j['time'] = int(time.time())
        str = json.dumps(j) + '\0'
        self.transport.write(str.encode('GB18030'))
        logger.info(f'发送数据到往{self.transport.getPeer().host}:{str.encode("GB18030")}')

    @Interval('3/second')
    def heart_beat(self):
        j = {}
        j['MSG'] = 0
        j['alive'] = 0
        import time
        j['time'] = int(time.time())
        str = json.dumps(j) + '\0'
        self.transport.write(str.encode('GB18030'))
        logger.info(f'发送数据到往{self.transport.getPeer().host}:{str.encode("GB18030")}')

    def query_all_device_data(self):
        j = {}
        j['MSG'] = 160
        j['oid'] = 0
        j['sdm'] = '192.168.3.24'
        j['owners'] = None
        str = json.dumps(j) + '\0'
        self.transport.write(str.encode('GB18030'))
        logger.info(f'发送数据到往{self.transport.getPeer().host}:{str.encode("GB18030")}')
