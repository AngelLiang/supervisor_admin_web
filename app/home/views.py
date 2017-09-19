#!/usr/bin/env python
# coding=utf-8
# Author: yannanxiu

import time
from flask import render_template, current_app, request
from flask_login import login_required
from . import home
from system_lib import *


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
    data["system"]["pstree"] = get_pstree()
    data["system"]["mem_info"] = get_mem_info()
    data["system"]["io_counters"] = get_io_counters()
    # _debug(data["system"]["cpu_stat"])

    data["network"]["iface_status"] = get_iface_status()
    data["network"]["connections"] = get_connections()

    return render_template("home/index.html", data=data)

# @home.teardown_app_request
# def _teardown_app_request(response):
#     now = time.time()
#     ip = request.remote_addr
#     url = request.base_url
#     current_app.logger.info("{ip} {now} {url}".format(ip=ip, now=now, url=url))
#     return response
