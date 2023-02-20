# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/2/27 21:15
# @Function: notion 基础信息处理


from sync_data.utils import log_detail


class NotionBaseInfo:
    """
    notion基础信息
    """
    def __init__(self, token):
        log_detail.debug("【Notion】notion参数初始化...")
        self.__base_url = "https://api.notion.com"
        self.__database_url = self.__base_url + "/v1/databases"
        self.__page_url = self.__base_url + "/v1/pages"
        self.__blocks_url = self.__base_url + "/v1/blocks"
        self.__users_url = self.__base_url + "/v1/users"
        self.__search_url = self.__base_url + "/v1/search"
        self.__headers = {'Authorization': f'Bearer {token}',
                        'Notion-Version': '2022-02-22',
                        "Content-Type": "application/json"}
        log_detail.debug("【Notion】notion完成初始化")

    def get_db_url(self):
        return self.__database_url

    def get_page_url(self):
        return self.__page_url

    def get_blocks_url(self):
        return self.__blocks_url

    def get_user_url(self):
        return self.__users_url

    def get_search_url(self):
        return self.__search_url

    def get_headers(self):
        return self.__headers

