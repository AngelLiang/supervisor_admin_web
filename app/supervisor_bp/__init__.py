#!/usr/bin/env python3
# coding=utf-8

from flask import Blueprint
supervisor = Blueprint('supervisor_bp', __name__)

from . import views
