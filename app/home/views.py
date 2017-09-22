#!/usr/bin/env python
# coding=utf-8
# Author: yannanxiu

import time
from flask import render_template, current_app, request, jsonify
from flask_login import login_required
from . import home
from system_lib import *
from .models import CPULoad, MemoryInfo


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

    return render_template("home/index.html", data=data)


@home.route("/json/cpu")
@login_required
def json_cpu():
    ret_json = {"status": 1}
    ret_json["request"] = request.base_url

    cpu_load = CPULoad.query.all()
    current_app.logger.debug(cpu_load)

    data = []
    for item in cpu_load:
        temp = {}
        time_str = str(item.datetime)
        temp[time_str] = {}
        temp[time_str]["1min"] = item.one
        temp[time_str]["3min"] = item.two
        temp[time_str]["5min"] = item.three
        data.append(temp)

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
