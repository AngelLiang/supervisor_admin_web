#!/usr/bin/env python
# coding=utf-8
"""
Blog: https://github.com/Supervisor/supervisor/blob/master/docs/api.rst
"""
import os
import pprint

try:
    import xmlrpclib
    from xmlrpclib import ProtocolError
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

# 获取当前路径
curr_dir = os.path.dirname(os.path.realpath(__file__))


class Supervisor():
    host = "127.0.0.1"
    port = 9001
    username = ""
    password = ""
    _server = None
    is_login = False

    def __init__(self):
        self.file = os.path.join(curr_dir, "config.ini")
        self.load_config()
        self.login()

    def load_config(self):
        if not os.path.isfile(self.file):
            return
        config = ConfigParser()
        config.readfp(open(self.file))
        self.host = config.get("supervisor", "host")
        self.port = config.getint("supervisor", "port")
        self.username = config.get("supervisor", "username")
        self.password = config.get("supervisor", "password")

    def save_config(self):
        config = ConfigParser()
        config.add_section("supervisor")
        config.set("supervisor", "host", self.host)
        config.set("supervisor", "port", self.port)
        config.set("supervisor", "username", self.username)
        config.set("supervisor", "password", self.password)
        config.write(open(self.file, "w"))

    def login(self):
        self.url = "http://{username}:{password}@{host}:{port}/RPC2".format(
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self._server = xmlrpclib.Server(self.url)
        try:
            ret = self._server.supervisor.getState()
        except ProtocolError:
            self.is_login = False
            ret = None
        except:
            self.is_login = False
            ret = None
        else:
            self.is_login = True
            self.save_config()
        return ret

    def listMethods(self):
        """查询API支持的方法"""
        return self._server.system.listMethods()

    def methodHelp(self, name):
        """查询方法文档"""
        return self._server.system.methodHelp(name)

    def getState(self):
        return self._server.supervisor.getState()

    def getAllProcessInfo(self):
        """查看所有进程"""
        return self._server.supervisor.getAllProcessInfo()

    def getProcessInfo(self, name):
        """查看某个进程的详细信息"""
        return self._server.supervisor.getProcessInfo(name)

    def startProcess(self, name):
        """启动某个进程"""
        return self._server.supervisor.startProcess(name)

    def stopProcess(self, name):
        """停止某个进程"""
        return self._server.supervisor.stopProcess(name)

    def startAllProcesses(self):
        """启动所有进程"""
        return self._server.supervisor.startAllProcesses()

    def stopAllProcesses(self):
        """停止所有进程"""
        return self._server.supervisor.stopAllProcesses()

    def readProcessLog(self, name, offset, length):
        return self._server.supervisor.readProcessLog(name, offset, length)

    def readProcessStdoutLog(self, name, offset, length):
        return self._server.supervisor.readProcessStdoutLog(name, offset, length)

    def clearProcessLog(self, name):
        """清除进程的日志"""
        return self._server.supervisor.clearProcessLog(name)


singleton_supervisor = Supervisor()


def test():
    print(singleton_supervisor.host, singleton_supervisor.port)
    print(singleton_supervisor.file)

    # allProInfo = supervisor.getAllProcessInfo()
    # pprint.pprint(allProInfo)
    ret = singleton_supervisor.login()
    print(ret)
    if not ret:
        return
    methods = singleton_supervisor.listMethods()
    print(methods)

    ret = singleton_supervisor.methodHelp("supervisor.clearProcessLog")
    print(ret)

    # ret = supervisor.stopProcess("IoT_Platform")
    # print(ret)

    # ret = supervisor.startProcess("IoT_Platform")
    # print(ret)

    # log = singleton_supervisor.readProcessStdoutLog("IoT_redis_clean", 0, 0)
    # print(log)


if __name__ == '__main__':
    test()
