#!/usr/bin/env python
# coding=utf-8
# Author: yannanxiu

import time
import datetime
from flask import render_template, current_app, request, jsonify
from flask_login import login_required
from . import home
from system_lib import *
from .models import CPULoad, MemoryInfo


def local2utc(local_st):
    """本地时间转UTC时间（-8:00）"""
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st


def _cpu_info_get():
    cpu_load = CPULoad.query.all()

    data = []
    for item in cpu_load:
        temp = {}
        time_str = str(item.datetime)
        temp[time_str] = {}
        temp[time_str]["1min"] = item.one
        temp[time_str]["3min"] = item.two
        temp[time_str]["5min"] = item.three
        data.append(temp)
    return data


def _stats_cpu_chartkick_get(limit=None):
    if limit:
        cpu_load = CPULoad.query.all()[-limit:]
    else:
        cpu_load = CPULoad.query.all()

    data = [
        {"name": "1min", "data": {}},
        {"name": "3min", "data": {}},
        {"name": "5min", "data": {}},
    ]
    for item in cpu_load:
        utc_time = local2utc(item.datetime)
        time_str = str(utc_time)

        data[0]["data"][time_str] = item.one
        data[1]["data"][time_str] = item.two
        data[2]["data"][time_str] = item.three

    return data


M = (1024 * 1024)


def _stats_mem_chartkick_get(limit=None):
    if limit:
        mem = MemoryInfo.query.all()[-limit:]
    else:
        mem = MemoryInfo.query.all()

    data = [
        {"name": "used", "data": {}},
        {"name": "free", "data": {}}
    ]
    for item in mem:
        utc_time = local2utc(item.datetime)
        time_str = str(utc_time)

        data[0]["data"][time_str] = item.used / M
        data[1]["data"][time_str] = item.free / M

    return data


@home.route("/")
@home.route("/index")
@login_required
def index():
    _debug = current_app.logger.debug

    data = {"basic": {}, "system": {}, "network": {}}
    data["basic"]["general"] = get_general()
    data["basic"]["cpu_info"] = get_cpu_info()
    data["basic"]["disk_info"] = get_disk_info()
    data["basic"]["net_info"] = get_net_info()
    # _debug(data["basic"]["net_info"])

    data["system"]["loadavg"] = get_loadavg()
    data["system"]["cpu_stat"] = get_cpu_stat()
    data["system"]["processes"] = get_intensive_processes()
    # data["system"]["pstree"] = get_pstree()
    # data["system"]["mem_info"] = get_mem_info()
    # data["system"]["io_counters"] = get_io_counters()
    # _debug(data["system"]["cpu_stat"])

    data["network"]["iface_status"] = get_iface_status()
    data["network"]["connections"] = get_connections()

    stats_cpu = _stats_cpu_chartkick_get(120)
    # current_app.logger.debug(stats_cpu)

    stats_mem = _stats_mem_chartkick_get(120)
    current_app.logger.debug(stats_mem)

    return render_template("home/index.html", data=data, stats_cpu=stats_cpu, stats_mem=stats_mem)


@home.route("/json/cpu")
@login_required
def json_cpu():
    ret_json = {"status": 1}
    ret_json["request"] = request.base_url

    data = _cpu_info_get()
    current_app.logger.debug(data)
    ret_json["data"] = data

    return jsonify(ret_json)


@home.route("/json/mem")
@login_required
def json_mem():
    ret_json = {"status": 1}
    ret_json["request"] = request.base_url

    mem = MemoryInfo.query.all()
    current_app.logger.debug(mem)

    data = []
    for item in mem:
        temp = {}
        time_str = str(item.datetime)
        temp[time_str] = {}
        temp[time_str]["used"] = item.used
        temp[time_str]["free"] = item.free
        data.append(temp)

    ret_json["data"] = data

    return jsonify(ret_json)
