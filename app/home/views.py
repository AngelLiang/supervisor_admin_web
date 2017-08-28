#!/usr/bin/env python
# coding=utf-8
# Author: yannanxiu

from  flask import render_template, current_app
from flask_login import login_required

from tools.cpustatus import CPUinfo, load_stat, meminfo
from . import home


@home.route("/")
@home.route("index")
@login_required
def index():
    cpuInfo = CPUinfo()
    loadStat = load_stat()
    memInfo = meminfo()

    current_app.logger.debug(cpuInfo)
    current_app.logger.debug(loadStat)
    current_app.logger.debug(memInfo)

    return render_template("home/index.html", cpuInfo=cpuInfo, loadStat=loadStat, memInfo=memInfo)

