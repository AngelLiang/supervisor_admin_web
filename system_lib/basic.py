# coding: utf-8

from __future__ import unicode_literals
import datetime
import platform
import socket
import subprocess
from .util import bytes2human
from collections import OrderedDict
import psutil
from uptime import uptime


def _seconds2human(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    time_str = '{0}days, {1}hours, {2}minutes, {3}seconds'.format(int(d), int(h), int(m), int(s))
    return time_str


def get_general():
    """
    获取通用信息
    :return: dict
        hostname - 主机名称
        os_name - 操作系统
        os_version - 系统版本
        server_time - 当前时间
        sys_up - 运行时间
    """
    dic = OrderedDict()
    dic["hostname"] = socket.gethostname()
    dic["os_name"] = platform.system()
    dic["os_version"] = platform.release()
    dic["server_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dic["sys_up"] = _seconds2human(uptime())

    return dic


def get_disk_info():
    """
    获取硬盘信息
    :return: list
        device - 设备
        mountpoint - 挂载点
        fstype - 文件系统
        total - 总容量
        used - 已使用容量
        free - 未使用容量
        percent - 使用百分比
    """
    disk_info = []

    partitions = psutil.disk_partitions(all=False)
    for partition in partitions:
        disk_usage = psutil.disk_usage(partition.mountpoint)
        disk_item = OrderedDict()
        disk_item["device"] = partition.device
        disk_item["mountpoint"] = partition.mountpoint
        disk_item["fstype"] = partition.fstype
        disk_item["total"] = bytes2human(disk_usage.total)
        disk_item["used"] = bytes2human(disk_usage.used)
        disk_item["free"] = bytes2human(disk_usage.free)
        disk_item["percent"] = disk_usage.percent

        disk_info.append(disk_item)
    return disk_info


def get_cpu_info():
    """
    获取CPU信息
    :return: list
        architecture - CPU架构
        byte_order - 大小端格式
        cpu_mhz - 运行频率
        cpus - 核数
        l1d_cache - d-cache缓存
        l1i_cache - i-cache缓存
        l2_cache - L2缓存
        l3_cache - L3缓存
    """
    cmd = '/usr/bin/lscpu'
    out = subprocess.check_output(cmd, shell=True)
    cpu_info = OrderedDict()
    public_keys = ['Architecture', 'Byte Order', 'CPU MHz', 'CPU(s)']
    public_pattern = 'cache'

    for line in out.splitlines():
        line = line.decode("utf-8")
        k, v = [item.strip() for item in line.split(':')]
        if k in public_keys or k.find(public_pattern) != -1:
            k = k.replace(' ', '_').replace('(', '').replace(')', '').lower()
            cpu_info[k] = v
    return cpu_info


def get_net_info():
    """
    获取网络信息
    :return: list
        address - IP地址
        interface -
        netmask - 子网掩码
    """
    if_addrs = psutil.net_if_addrs()
    net_info = list()
    for interface, addrs in if_addrs.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                dic = OrderedDict()
                dic["interface"] = interface
                dic["address"] = addr.address
                dic["netmask"] = addr.netmask
                net_info.append(dic)

    return net_info
