#!/usr/bin/env python
# encoding=utf-8

__author__ = 'Vietronic'
__date__ = '$2018-7-23$'

import json


class DatabaseConfig:
    __name__ = 'DatabaseConfig'

    def __init__(self):
        # 初始化配置信息
        self.CONFIG_PATH = './config/database.json'
        # 加载配置文件
        f = open(self.CONFIG_PATH, 'r', encoding='utf-8')
        config = json.load(f)
        f.close()
        self.CONFIG = config
        return

    def database(self):
        return self.CONFIG["database"]

    def user(self):
        return self.CONFIG["user"]

    def password(self):
        return self.CONFIG["password"]

    def table(self):
        return self.CONFIG["table"]

    def host(self):
        return self.CONFIG["host"]

    def port(self):
        return self.CONFIG["port"]

    def init_tables_path(self):
        return self.CONFIG["init_tables_path"]


class ApiConfig:
    __name__ = 'ApiConfig'

    def __init__(self):
        # 初始化配置信息
        self.CONFIG_PATH = './config/api.json'
        # 加载配置文件
        f = open(self.CONFIG_PATH, 'r', encoding='utf-8')
        config = json.load(f)
        f.close()
        self.CONFIG = config
        return

    def api_key(self):
        return "?api_key=" + self.CONFIG["api_key"]

    def api_url(self):
        return self.CONFIG["api_url"]