#!/usr/bin/env python
# coding=utf-8
# Author: yannanxiu

from  flask import request, render_template
from . import home
from flask_login import login_required

@home.route("/")
@home.route("index")
@login_required
def index():
    return render_template("home/index.html")




