#!/usr/bin/env python
# coding=utf-8

import os
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


# =====================================================================================

from ConfigParser import ConfigParser

# 获取当前路径
curr_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(curr_dir, "config.ini")

singleton_admin = User()
config = ConfigParser()
config.readfp(open(config_file))
singleton_admin.id = 0
singleton_admin.username = config.get("admin_account", "username")
singleton_admin.password = config.get("admin_account", "password")


