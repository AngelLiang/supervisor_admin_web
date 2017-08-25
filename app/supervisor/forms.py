#!/usr/bin/env python
# coding=utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, IPAddress, NumberRange


class SupervisorLoginForm(FlaskForm):
    host = StringField(u"IP", validators=[DataRequired(), IPAddress])
    port = IntegerField(u"端口", validators=[DataRequired(), NumberRange(0, 65535)])
    username = StringField(u'用户名', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    submit = SubmitField(u'提交')

