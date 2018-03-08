#!/usr/bin/python2.7
#-*- coding:utf-8 -*-

import socket

class ToolHost(object):
    @staticmethod
    def get_ip_address():
        host_name = socket.getfqdn(socket.gethostname())
        ip_addr = socket.gethostbyname(host_name)
        return ip_addr
