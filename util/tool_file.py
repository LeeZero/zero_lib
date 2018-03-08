#!/usr/bin/python
# -*- coding:utf-8 -*-

import threading
import hashlib

class FileSaver(object):
    def __init__(self, fn, is_truncate=False):
        self.fd = open(fn, 'a+b')
        self.lock = threading.Lock()
        if is_truncate:
            self.fd.truncate()

    def re_open(self, fn):
        with self.lock:
            self.fd.close()
            self.fd = open(fn, 'a+b')

    def __del__(self):
        self.fd.close()

    def append(self, value):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        with self.lock:
            self.fd.write(value + "\n")
            self.fd.flush()

    def info(self, value):
        self.append(value)

class HashUtil(object):
    @staticmethod
    def get_md5(string):
        return hashlib.md5(string).hexdigest()

    @staticmethod
    def get_unicode_md5(unicode_str):
        return hashlib.md5(unicode_str.encode("utf-8")).hexdigest()
