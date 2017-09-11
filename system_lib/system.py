# coding: utf-8

from __future__ import unicode_literals
import datetime
import socket
from collections import OrderedDict
from .util import obj2dict
from .const import SOCK_TYPE
import psutil

M = 1024 * 1024


def get_loadavg():
    """
    获取CPU负载信息
    :return: dict
        1min - 最近1分钟CPU负载
        3min - 最近3分钟CPU负载
        5min - 最近5分钟CPU负载
    """
    load_file = '/proc/loadavg'

    with open(load_file, 'r') as lfp:
        line = lfp.readline()
        items = [item.strip() for item in line.split(' ') if item.strip()]
        dic = OrderedDict()
        dic["1min"] = float(items[0]) * 100
        dic["3min"] = float(items[1]) * 100
        dic["5min"] = float(items[2]) * 100
        return dic


def _parse_cpu_fields(fields):
    field_list = [int(field) for field in fields]
    total = sum(field_list)
    return {
        'total': total,
        'user': field_list[1],
        'nice': field_list[2],
        'system': field_list[2],
        'idle': field_list[3],
        'busy': 100 - field_list[3],
        'iowait': field_list[4],
        'irq': field_list[5],
        'soft_irq': field_list[6],
        'steal': field_list[7],
        'guest': field_list[8]
    }


def get_cpu_stat():
    """
    获取CPU状态信息
    :return: dict
    """
    cpu_stat_file = '/proc/stat'

    cpu_stat = OrderedDict(cpus=OrderedDict())
    with open(cpu_stat_file, 'r') as cfp:
        for line in cfp:
            fields = [field.strip() for field in line.split(' ') if field.strip()]
            if len(fields) < 2:
                continue

            field_name = fields[0]
            if field_name.startswith('cpu'):
                cpu_stat['cpus'][field_name] = _parse_cpu_fields(fields[1:])
            elif field_name in ['ctxt', 'processes', 'procs_running', 'procs_blocked']:
                cpu_stat[field_name] = int(fields[1])

    return cpu_stat


def _proc2simple(proc):
    with proc.oneshot():
        return {
            'pid': proc.pid,
            'name': proc.name(),
            'username': proc.username(),
            'create_time': datetime.datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
            'cpu_percent': round(proc.cpu_percent(), 2),
            'memory_percent': round(proc.memory_percent(), 2),
            'status': proc.status()
        }


def get_intensive_processes():
    """
    获取占用CPU和内存前十个最高/最多的进程
    :return:
    """
    procs = list(map(_proc2simple, psutil.process_iter()))

    # cpu_intensive = sorted(procs, cmp=lambda x, y: x['cpu_percent'] < y['cpu_percent'], reverse=True)[0: 10]
    cpu_intensive = sorted(procs, key=lambda x: x['cpu_percent'], reverse=True)[0: 10]
    # mem_intensive = sorted(procs, cmp=lambda x, y: x['memory_percent'] < y['memory_percent'], reverse=True)[0:10]
    mem_intensive = sorted(procs, key=lambda x: x['memory_percent'], reverse=True)[0:10]

    dic = OrderedDict()
    dic["cpu_intensive"] = cpu_intensive
    dic["mem_intensive"] = mem_intensive
    return dic


def get_simple_process(pids):
    simple_process = []
    for process in psutil.process_iter():
        if pids and process.pid not in pids:
            continue

        simple_process.append(_proc2simple(process))

    return simple_process


def get_children(nodes_dict, parent):
    nodes = nodes_dict[parent]
    children = list()

    for child in nodes:
        dic = OrderedDict()
        dic["process"] = child
        dic["children"] = get_children(nodes_dict, child)
        children.append(dic)

    return children


def transfer_nodes2tree(nodes_dict, child_nodes):
    tree = list()
    for parent, cur_children in list(nodes_dict.items()):
        if parent not in child_nodes:  # first level
            # dic = OrderedDict()
            tree.append({
                'process': parent,
                'children': get_children(nodes_dict, parent)
            })
    return tree


def conn2json(conn):
    laddr = list(map(str, conn.laddr))
    raddr = list(map(str, conn.raddr))
    return {
        'fd': conn.fd,
        'laddr': ':'.join(laddr),
        'raddr': ':'.join(raddr),
        'status': conn.status,
        'type': SOCK_TYPE.get(socket.SOCK_STREAM, 'raw')
    }


def get_pstree():
    """
    获取进程树
    :return:
    """
    nodes_dict = OrderedDict()
    child_nodes = []
    for process in psutil.process_iter():
        cur_child_nodes = ['{0}-{1}'.format(child.pid, child.name()) for child in process.children()]
        nodes_dict['{0}-{1}'.format(process.pid, process.name())] = cur_child_nodes
        child_nodes.extend(cur_child_nodes)

    return transfer_nodes2tree(nodes_dict, child_nodes)


def children_processor(children):
    return [{'pid': child.pid,
             'name': child.name(),
             'status': child.status(),
             'create_time': datetime.datetime.fromtimestamp(
                 child.create_time()).strftime("%Y-%m-%d %H:%M:%S")} for child in children]


def get_process_detail(pid):
    for process in psutil.process_iter():
        if process.pid == pid:
            cur_process = process
            break
    else:
        raise Exception('No such process: {0}'.format(pid))

    override = {
        type(cur_process): {
            'children': children_processor,
            'parent': lambda p: {'pid': p.pid, 'name': p.name()} if p else None,
            'cmdline': lambda lines: ' '.join(lines),
            'connections': lambda conns: list(map(conn2json, conns)),
            'create_time': lambda timestamp: datetime.datetime.fromtimestamp(
                timestamp).strftime("%Y-%m-%d %H:%M:%S")
        }
    }

    ignore = {
        type(cur_process): ['kill', 'oneshot', 'environ', 'send_signal', 'suspend',
                            'as_dict', 'uids', 'gids', 'terminal', 'is_running',
                            'ionice', 'rlimit', 'memory_info_ex', 'memory_info',
                            'resume', 'terminate', 'wait', 'memory_maps']
    }

    return obj2dict(cur_process, methods=True,
                    override=override, ignore=ignore)


def search_process(q):
    process_list = []
    for process in psutil.process_iter():
        name = process.name()
        cmdline = ''.join(process.cmdline())
        if name != '' and name.find(q) != -1:
            idx = name.find(q)
            process_list.append('{0}-{1}'.format(process.pid, name))
        elif cmdline != '' and cmdline.find(q) != -1:
            idx = cmdline.find(q)
            process_list.append('{0}-{1}'.format(process.pid, cmdline[idx:]))
        elif str(process.pid).find(q) != -1:
            process_list.append('{0}-{1}'.format(process.pid, name))

    return process_list


def get_mem_info():
    """
    获取内存信息，单位为M
    :return:
    """
    memory = psutil.virtual_memory()
    dic = OrderedDict()
    dic["total"] = round(memory.total / M, 2)
    dic["available"] = round(memory.available / M, 2)
    dic["active"] = round(memory.active / M, 2)
    dic["free"] = round(memory.free / M, 2)
    dic["buffers"] = round(memory.buffers / M, 2)
    dic["cached"] = round(memory.cached / M, 2)
    dic["percent"] = round(memory.percent, 2)
    return dic


def get_io_counters():
    """
    获取IO统计
    :return:
    """
    io_counters = psutil.disk_io_counters()
    dic = OrderedDict()
    dic["read_count"] = io_counters.read_count
    dic["read_bytes"] = io_counters.read_bytes
    dic["write_count"] = io_counters.write_count
    dic["write_bytes"] = io_counters.write_bytes
    dic["read_time"] = io_counters.read_time
    dic["write_time"] = io_counters.write_time

    return dic
