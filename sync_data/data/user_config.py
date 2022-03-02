# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/2/28 23:12
# @Function:

from enum import Enum


class ConfigName(Enum):
    USER_AGENT = "user_agent"
    DOUBAN = "douban"
    DOUBAN_USER_ID = 'user_id'

    NOTION = "notion"
    NOTION_TOKEN = 'token'
    NOTION_PAGE_ID = 'page_id'
    NOTION_BOOK = 'book_database_id'
    NOTION_MUSIC = 'music_database_id'
    NOTION_TV = 'tv_database_id'
    NOTION_MOVIE = 'movie_database_id'


class UserConfig(object):

    def __init__(self):
        self.user_agent = ''
        self.douban = {}
        self.notion = {}
