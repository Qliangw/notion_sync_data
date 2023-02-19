# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/2/28 23:12
# @Function:

from enum import Enum


class ConfigName(Enum):
    USER_AGENT = "user_agent"
    USER_COOKIE = "cookies"
    DOUBAN = "douban"
    DOUBAN_USER_ID = 'user_id'
    DOUBAN_DAY = "day"

    NOTION = "notion"
    NOTION_TOKEN = 'token'
    NOTION_PAGE_ID = 'page_id'
    NOTION_BOOK = 'book_database_id'
    NOTION_MUSIC = 'music_database_id'
    NOTION_MOVIE = 'movie_database_id'
    NOTION_GAME = 'game_database_id'


class UserConfig(object):

    def __init__(self):
        self.user_agent = ''
        self.douban = {}
        self.notion = {}

def get_desensitization_of_user_info(user_info):
    x_user_info = ''
    user_len = len(user_info)
    for i in range(user_len):
        if user_len / 2 - user_len / 4 < i < user_len / 2 + user_len / 4:
            x_user_info += "*"
        else:
            x_user_info += user_info[i]
    return x_user_info
