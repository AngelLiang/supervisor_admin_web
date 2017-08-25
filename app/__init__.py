#!/usr/bin/env python
# coding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
bootstrap = Bootstrap()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = u"请先登录！"

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    db.app = app

    bootstrap.init_app(app)
    login_manager.init_app(app)

    # 注册蓝本
    from app.home import home
    app.register_blueprint(home, url_prefix="/")

    # 增加auth蓝本
    from app.auth import auth
    app.register_blueprint(auth, url_prefix="/auth")

    from app.supervisor import supervisor
    app.register_blueprint(supervisor, url_prefix='/supervisor')

    # 附加路由和自定义的错误页面
    from errors import error_404, error_500
    app.register_error_handler(404, error_404)
    app.register_error_handler(500, error_500)

    return app

