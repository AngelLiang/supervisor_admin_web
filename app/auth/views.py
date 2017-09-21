#!/usr/bin/env python
# coding=utf-8


from flask import url_for, redirect, render_template, flash
from flask_login import login_user, login_required, logout_user
from .models import User, singleton_admin

from . import auth
from .forms import LoginForm
from supervisior_lib.supervisor import singleton_supervisor as supervisor


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if "admin"== username and singleton_admin.verify_password(password):
                login_user(singleton_admin)
                return redirect(url_for("home.index"))
        else:
            flash(u"登录失败", category="error")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    user_id = int(user_id)
    if 0==user_id:
        return singleton_admin
    return User.query.get(user_id)

