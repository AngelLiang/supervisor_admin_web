#!/usr/bin/env python
# coding=utf-8

from flask import render_template, request
from flask_login import login_required
from pprint import pprint
from .. import redis_store
from . import redis as red
from redis_lib.redis_lib import RedisMonitor


@red.route("/")
@login_required
def index():
    ret_info = redis_store.info()
    # pprint(ret_info)
    data = RedisMonitor.info_handle(ret_info)
    # pprint(data)
    return render_template("redis/info.html", data=data)
