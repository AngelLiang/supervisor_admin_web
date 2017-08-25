#!/usr/bin/env python
# coding=utf-8

from flask import current_app, render_template

# @current_app.app_errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404

# @current_app.app_errorhandler(500)
def error_500(e):
    return render_template('500.html'), 500

