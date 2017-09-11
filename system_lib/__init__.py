# coding: utf-8

from __future__ import unicode_literals
import platform

if "Linux" != platform.system():
    raise EnvironmentError(u"该库用于Linux环境")

from .basic import get_general, get_cpu_info, get_disk_info, get_net_info
from .system import get_loadavg, get_cpu_stat, get_intensive_processes, get_pstree, get_mem_info, get_io_counters
from .network import get_iface_status, get_connections
