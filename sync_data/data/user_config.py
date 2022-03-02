# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/2/28 23:12
# @Function:

from enum import Enum


class ConfigName(Enum):
    USER_AGENT = "user_agent"
    DOUBAN = "douban"
    NOTION = "notion"
    DOUBAN_USER_ID = 'user_id'


class UserConfig(object):

    def __init__(self):
        self.user_agent = ''
        self.douban = {}
        self.notion = {}
