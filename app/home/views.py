#!/usr/bin/env python
# coding=utf-8
# Author: yannanxiu

from flask import render_template, current_app, request
from flask_login import login_required
from . import home
from system_lib import *


@home.route("/")
@home.route("/index")
@login_required
def index():
    _debug = current_app.logger.debug

    data = {"basic": {}, "system": {}, "netwotk": {}}
    data["basic"]["general"] = get_general()
    data["basic"]["cpu_info"] = get_cpu_info()
    data["basic"]["disk_info"] = get_disk_info()
    data["basic"]["net_info"] = get_net_info()
    _debug(data["basic"]["net_info"])

    data["system"]["loadavg"] = get_loadavg()
    data["system"]["cpu_stat"] = get_cpu_stat()
    data["system"]["processes"] = get_intensive_processes()
    data["system"]["pstree"] = get_pstree()
    data["system"]["mem_info"] = get_mem_info()
    data["system"]["io_counters"] = get_io_counters()
    # _debug(data["system"]["cpu_stat"])

    return render_template("home/index.html", data=data)


@home.after_request
def home_after_request(response):
    ip = request.remote_addr
    url = request.base_url
    current_app.logger.info("{ip} {url}".format(ip=ip, url=url))
    return response
