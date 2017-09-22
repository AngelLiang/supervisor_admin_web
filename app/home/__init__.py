#!/usr/bin/env python
# coding=utf-8

from flask import Blueprint

home = Blueprint('home', __name__)

from .models import *
from . import views
