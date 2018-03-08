#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import ConfigParser

class ToolMysqlClient(object):

    def __init__(self, **kwargs):
        self._mysql_host = None
        self._mysql_port = None
        self._mysql_user = None
        self._mysql_passwd = None
        self._mysql_db_str = None
        self._mysql_auto_commit = None

        if kwargs.get("cfg_cn"):
            self.__read_configure(kwargs.get("cfg_cn"))
        else:
            self._mysql_host = kwargs.get("mysql_host")
            self._mysql_port = kwargs.get("mysql_port")
            self._mysql_user = kwargs.get("mysql_user")
            self._mysql_passwd = kwargs.get("mysql_passwd")
            self._mysql_db_str = kwargs.get("mysql_db")
            self._mysql_auto_commit = kwargs.get("auto_commit")

        self._connect()


    def __read_configure(self, cfg_fn="mysql.cfg"):
        cf = ConfigParser.ConfigParser()
        cf.read(filenames=cfg_fn)

        # mysql配置
        self._mysql_host = cf.get("mysql", "mysql_host")
        self._mysql_port = cf.getint("mysql", "mysql_port")
        self._mysql_user = cf.get("mysql", "mysql_user")
        self._mysql_passwd = cf.get("mysql", "mysql_passwd")
        self._mysql_db_str = cf.get("mysql", "mysql_db")
        self._mysql_auto_commit = cf.getboolean("mysql", "auto_commit")

    def _connect(self):
        self._con = MySQLdb.connect(host=self._mysql_host, user=self._mysql_user, passwd=self._mysql_passwd,
                                    db=self._mysql_db_str, port=self._mysql_port, autocommit=self._mysql_auto_commit)
        self._con.set_character_set('utf8')
        self._cursor = self._con.cursor()

    def get_cursor(self):
        return self._cursor

    def insert(self, sql_insert, dict):
        self._cursor.execute(sql_insert, dict)

    def excute(self, sql_str):
        self._cursor.execute(sql_str)

    def commit(self):
        self._con.commit()

    def close(self):
        self._cursor.close()
        self._con.close()

    def insert_dict(self, table, dict):
        values = ', '.join(['%s'] * len(dict))
        cols = ', '.join(dict.keys())
        sql_insert = "INSERT INTO %s (%s) VALUES (%s)"%(table, cols, values)
        self._cursor.execute(sql_insert, dict.values())

    def get_con(self):
        return self._con

    def reconnect(self):
        self._connect()

