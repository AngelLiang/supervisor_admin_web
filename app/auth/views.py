#!/usr/bin/env python
# coding=utf-8


from flask import url_for, redirect, render_template, flash
from . import auth

from .forms import LoginForm
from supervisior_api.supervisor import singleton_supervisor as supervisor


@auth.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        ret = supervisor.login(username, password)
        if ret:
            flash(u"登录成功")
            return redirect(url_for("supervisor.index"))
        else:
            flash(u"登录失败", category="error")
    return render_template("auth/login.html", form=form)
