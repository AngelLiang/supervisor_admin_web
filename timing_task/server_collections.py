#!/usr/bin/env python
# coding=utf-8

import datetime as dt
import psutil
from apscheduler.schedulers.blocking import BlockingScheduler
from system_lib import *
from manage import db
from app.home.models import CPULoad, MemoryInfo

task = BlockingScheduler()

KB = 1024
M = (1024 * 1024)


@task.scheduled_job(trigger="interval", id="cpu", seconds=60)
def cpu_info_get_task():
    now = dt.datetime.now()

    cpu_load = get_loadavg()
    one = cpu_load.get("1min")
    two = cpu_load.get("3min")
    three = cpu_load.get("5min")

    print(str(now) + " {} {} {}".format(one, two, three))

    cpu = CPULoad()
    cpu.datetime = now
    cpu.one = one
    cpu.two = two
    cpu.three = three
    db.session.add(cpu)
    db.session.commit()


@task.scheduled_job(trigger="interval", id="mem", seconds=60)
def memory_info_get_task():
    now = dt.datetime.now()

    # mem = get_mem_info()
    mem = psutil.virtual_memory()

    used = mem.used
    free = mem.free

    print(str(now) + " {}M {}M".format(round(used / M, 2), round(free / M, 2)))

    mem_info = MemoryInfo()
    mem_info.datetime = now
    mem_info.used = used
    mem_info.free = free
    db.session.add(mem_info)
    db.session.commit()


@task.scheduled_job(trigger="interval", id="clean", seconds=60)
def clean_task():
    now = dt.datetime.now()
    cut_time = dt.timedelta(days=3)
    cut = now - cut_time

    cpu = CPULoad.query.filter(CPULoad.datetime < cut).all()
    for item in cpu:
        db.session.delete(item)

    mem = MemoryInfo.query.filter(MemoryInfo.datetime < cut).all()
    for item in mem:
        db.session.delete(item)

    print("delete")
    print(cpu, mem)
    db.session.commit()


if __name__ == '__main__':
    task.start()
