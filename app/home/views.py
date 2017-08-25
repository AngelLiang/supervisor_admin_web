#!/usr/bin/env python
# coding=utf-8
# Author: yannanxiu

from  flask import request, render_template
from . import home

@home.route("/")
@home.route("index")
def index():
    return render_template("home/index.html")




