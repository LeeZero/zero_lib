#!/usr/bin/python
# -*- coding: utf-8 -*-

import redis
import json
from ConfigParser import ConfigParser

class ToolRedisClient(object):
    def __init__(self, cfg_fn):
        self._redis_host = None
        self._redis_port = None
        self._redis_passwd = None
        self._redis_db = None
        self._redis_topic = None

        self.__read_configure(cfg_fn)
        self._redis = redis.StrictRedis(host=self._redis_host, port=self._redis_port, password=self._redis_passwd, db=self._redis_db)

    def __read_configure(self, cfg_fn="redis.cfg"):
        cf = ConfigParser()
        cf.read(filenames=cfg_fn)

        # redis配置
        self._redis_host = cf.get("redis", "redis_host")
        self._redis_port = cf.getint("redis", "redis_port")
        self._redis_passwd = cf.get("redis", "redis_passwd")
        self._redis_db = cf.get("redis", "redis_db")
        self._redis_topic = cf.get("redis", "redis_topic")

    def get_redis_client(self):
        return self._redis

    def pub_topic(self, msg_list):
        msg_str = json.dumps(msg_list, ensure_ascii=False)
        self._redis.publish(self._redis_topic, msg_str)

    def sub_topic_channel(self):
        ps = self._redis.pubsub()
        ps.subscribe(self._redis_topic)
        return ps

    def produce_msg(self, msg_list):
        msg_str = json.dumps(msg_list, ensure_ascii=False)
        self._redis.lpush(self._redis_topic, msg_str)

    def consume_msg(self):
        msg = self._redis.brpop(self._redis_topic, 0)
        return msg

