#!/usr/bin/env python
# coding=utf-8


from flask import request, render_template, redirect, url_for, current_app, flash
from flask_login import login_required
from . import supervisor as sup_bp
from supervisior_lib.supervisor import singleton_supervisor as supervisor
from .forms import SupervisorLoginForm


@sup_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = SupervisorLoginForm()
    if form.validate_on_submit():
        supervisor.host = form.host.data
        supervisor.port = form.port.data
        supervisor.username = form.username.data
        supervisor.password = form.password.data
        ret = supervisor.login()
        if ret:
            flash(u"登录成功！")
        else:
            flash(u"登录失败！", category="error")

    return render_template("supervisor/index.html", form=form, supervisor=supervisor)


@sup_bp.route("/add", methods=["GET", "POST"])
@login_required
def sup_add():
    current_app.logger.debug(request.values)
    return redirect(url_for("supervisor_bp.index"))


@sup_bp.route("/process_start")
@login_required
def process_start():
    args = request.args
    current_app.logger.debug(args)
    name = args.get("name")
    if name:
        ret = supervisor.startProcess(name)
        current_app.logger.debug(ret)
        if True == ret:
            flash(name + u"启动成功！", )
        else:
            flash(name + u"启动失败！", "errors")

    return redirect(url_for("supervisor_bp.index"))


@sup_bp.route("/process_stop")
@login_required
def process_stop():
    args = request.args
    current_app.logger.debug(args)
    name = args.get("name")
    if name:
        ret = supervisor.stopProcess(name)
        current_app.logger.debug(ret)
        if True == ret:
            flash(name + u"停止成功！", )
        else:
            flash(name + u"停止失败！", "errors")

    return redirect(url_for("supervisor_bp.index"))


@sup_bp.route("/processLog_clear")
@login_required
def processLog_clear():
    args = request.args
    current_app.logger.debug(args)
    name = args.get("name")
    if name:
        ret = supervisor.clearProcessLog(name)
        current_app.logger.debug(ret)
        if ret:
            flash(u"清除成功！")
    return redirect(url_for("supervisor_bp.index"))


@sup_bp.route("/processLog_read")
@login_required
def processLog_read():
    args = request.args
    current_app.logger.debug(args)
    name = args.get("name")
    response = "<pre></per>"
    if name:
        name.strip()
        ret = supervisor.readProcessLog(name, -1024, 0)
        if ret:
            current_app.logger.debug(ret)
            response = "<pre>" + ret + "</pre>"
    if request.is_xhr:
        pass
    return response
