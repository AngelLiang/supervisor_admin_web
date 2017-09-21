#!/usr/bin/env python
# coding=utf-8

from flask import Blueprint
redis = Blueprint('redis_bp', __name__)

from . import views