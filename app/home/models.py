#!/usr/bin/env python
# coding=utf-8

import datetime as dt
from app import db


class CPULoad(db.Model):
    __tablename__ = 'cpu_load'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    one = db.Column(db.Float)  # 1min
    two = db.Column(db.Float)  # 3min
    three = db.Column(db.Float)  # 5min

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return '<{} {} {} {}>'.format(self.datetime, self.one, self.two, self.three)


class MemoryInfo(db.Model):
    __tablename__ = 'memory_info'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Integer)  # 已经使用，单位为Byte
    free = db.Column(db.Integer)  # 未使用，单位为Byte

    def __repr__(self):
        return '<{} {} {}>'.format(self.datetime, self.used, self.free)


class DeviceInfo(db.Model):
    __tablename__ = 'device_info'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Integer)  # 已经使用
    free = db.Column(db.Integer)  # 未使用
    cached = db.Column(db.Integer)
