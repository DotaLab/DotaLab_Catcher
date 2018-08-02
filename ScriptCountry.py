#!/usr/bin/env python
# encoding=utf-8

# 此脚本为补全heroes表中的英雄头像url，但是只有104个url

__author__ = 'Vietronic'
__date__ = '$2018-7-31$'

import json
import requests
from Database import Database
from lxml import etree

# 页面下载函数
def getPage(url):
    # 错误处理机制防止获取页面出错
    try:
        # 获取页面
        temp = requests.get(url)
        # 如果响应状态码不是 200，就主动抛出异常
        temp.raise_for_status()
    except requests.RequestException as e:
        print(e)
        # 如果出错则返回空
        # return None
    else:
        # 返回获得的页面文本
        return temp.text

URL = "http://doc.chacuo.net/iso-3166-1"

page = getPage(URL)

# 将其解析为XML
textTree = etree.HTML(page)

# 获取最新消息链接
xpathKey = "//*[@id=\"main\"]/div/table/tbody/tr/td[1]/text()"
xpathValue = "//*[@id=\"main\"]/div/table/tbody/tr/td[6]/text()"

key = textTree.xpath(xpathKey)
value = textTree.xpath(xpathValue)

for i in range(len(key)):
    print(key[i], value[i]) 