#!/usr/bin/env python
# coding=utf-8


from __future__ import division
import redis, time
import sys, os
import socket
from pprint import pprint
from collections import OrderedDict

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

# 获取当前路径
curr_dir = os.path.dirname(os.path.realpath(__file__))


class RedisMonitor():
    host = ""
    port = 0

    def __init__(self):
        self._config_file = os.path.join(curr_dir, "config.ini")
        self.r = redis.Redis(self.host, self.port)

    def load_config(self):
        if not os.path.isfile(self._config_file):
            return
        config = ConfigParser()
        with open(self._config_file) as file:
            config.readfp(file)
            self.host = config.get("redis", "host")
            self.port = config.getint("redis", "port")

    def save_config(self):
        config = ConfigParser()
        config.add_section("redis")
        config.set("redis", "host", self.host)
        config.set("redis", "port", self.port)
        config.write(open(self._config_file, "w"))

    @staticmethod
    def server_info_get(info):
        ret = OrderedDict()
        ret["os"] = info.get("os")
        ret["arch_bits"] = info.get("arch_bits")
        return ret

    @staticmethod
    def redis_info_get(info):
        ret = OrderedDict()
        ret["run_id"] = info.get("run_id")
        ret["process_id"] = info.get("process_id")
        ret["tcp_port"] = info.get("tcp_port")
        ret["redis_version"] = info.get("redis_version")
        ret["uptime_in_seconds"] = info.get("uptime_in_seconds")
        ret["uptime_in_days"] = info.get("uptime_in_days")
        # ret["redis_version"] = info.get("redis_version")
        return ret

    @staticmethod
    def clients_info_get(info):
        ret = OrderedDict()
        ret["connected_clients"] = info.get("connected_clients")
        ret["client_biggest_input_buf"] = info.get("client_biggest_input_buf")
        ret["blocked_clients"] = info.get("blocked_clients")
        ret["client_longest_output_list"] = info.get("client_longest_output_list")
        return ret

    @staticmethod
    def cpu_info_get(info):
        ret = OrderedDict()
        ret["used_cpu_sys"] = info.get("used_cpu_sys")
        ret["used_cpu_user"] = info.get("used_cpu_user")
        ret["used_cpu_sys_children"] = info.get("used_cpu_sys_children")
        ret["used_cpu_user_children"] = info.get("used_cpu_user_children")
        return ret

    @staticmethod
    def memory_info_get(info, all=False):
        ret = OrderedDict()
        ret["used_memory_human"] = info.get("used_memory_human")
        ret["used_memory_peak_human"] = info.get("used_memory_peak_human")
        if all:
            ret["used_memory"] = info.get("used_memory")
            ret["used_memory_peak"] = info.get("used_memory_peak")
            ret["used_memory_rss"] = info.get("used_memory_rss")
            ret["used_memory_lua"] = info.get("used_memory_lua")
            ret["mem_fragmentation_ratio"] = info.get("mem_fragmentation_ratio")
            ret["mem_allocator"] = info.get("mem_allocator")
        return ret

    @staticmethod
    def stats_info_get(info):
        ret = OrderedDict()
        ret["total_connections_received"] = info.get("total_connections_received")
        ret["total_commands_processed"] = info.get("total_commands_processed")
        ret["instantaneous_ops_per_sec"] = info.get("instantaneous_ops_per_sec")
        ret["rejected_connections"] = info.get("rejected_connections")
        ret["expired_keys"] = info.get("expired_keys")
        ret["evicted_keys"] = info.get("evicted_keys")
        ret["keyspace_hits"] = info.get("keyspace_hits")
        ret["keyspace_misses"] = info.get("keyspace_misses")
        ret["pubsub_channels"] = info.get("pubsub_channels")
        ret["pubsub_patterns"] = info.get("pubsub_patterns")
        ret["latest_fork_usec"] = info.get("latest_fork_usec")
        return ret

    @staticmethod
    def info_handle(info):
        ret = OrderedDict()
        ret["server"] = RedisMonitor.server_info_get(info)
        ret["redis"] = RedisMonitor.redis_info_get(info)
        ret["client"] = RedisMonitor.clients_info_get(info)
        ret["cpu"] = RedisMonitor.cpu_info_get(info)
        ret["memory"] = RedisMonitor.memory_info_get(info)
        # ret["stats"] = RedisMonitor.stats_info_get(info)
        return ret


redis_monitor = RedisMonitor()


def test():
    # ret = getInfo()
    r = redis.Redis()
    ret = r.info()
    pprint(ret)


if __name__ == '__main__':
    test()
