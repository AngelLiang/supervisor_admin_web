# coding: utf-8

from __future__ import unicode_literals
import subprocess
from collections import OrderedDict


def get_connections():
    conn_cmd = 'netstat -natp'
    conn_out = subprocess.check_output(conn_cmd, shell=True)
    conn_lines = conn_out.splitlines()[2:]
    count = len(conn_lines)
    conns = {'conns': list(), 'count': count}
    for line in conn_lines:
        items = [item.strip() for item in line.split(' ') if item.strip()]
        dic = OrderedDict()
        dic["status"] = items[5]
        dic["recv_q"] = int(items[1])
        dic["send_q"] = int(items[2])
        dic["l_addr"] = items[3]
        dic["r_addr"] = items[4]
        dic["pid"] = items[6].split('/')[0]

        conns['conns'].append(dic)

    return conns


def get_iface_status():
    """
    获取网卡的状态
    :return: dict
    """
    iface_files = '/proc/net/dev'
    iface_info = OrderedDict()
    with open(iface_files, b'r') as ifp:
        lines = ifp.readlines()[2:]
        for line in lines:
            items = [item.strip() for item in line.split(' ') if item.strip()]

            iface_info[items[0][:-1]] = {
                'receive_bytes': int(items[1]),
                'receive_packets': int(items[2]),
                'send_bytes': int(items[9]),
                'send_packets': int(items[10])
            }

    return iface_info
