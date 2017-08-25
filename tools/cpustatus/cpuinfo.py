#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function
from collections import OrderedDict
import pprint
import platform


def getLinuxCPUinfo():
    CPUinfo = OrderedDict()
    procinfo = OrderedDict()

    nprocs = 0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                # end of one processor
                CPUinfo['proc%s' % nprocs] = procinfo
                nprocs = nprocs + 1
                # Reset
                procinfo = OrderedDict()
            else:
                if len(line.split(':')) == 2:
                    procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                else:
                    procinfo[line.split(':')[0].strip()] = ''
    return CPUinfo


def CPUinfo():
    if "Linux" == platform.system():
        return getLinuxCPUinfo()
    elif "Windows" == platform.system():
        pass



if __name__ == '__main__':
    cpuinfo = CPUinfo()
    pprint.pprint(cpuinfo)
    for processor in cpuinfo.keys():
        print(cpuinfo[processor]['model name'])
