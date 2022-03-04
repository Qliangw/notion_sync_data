# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/3/1 21:05
# @Function: 测试单元
import random

from bs4 import BeautifulSoup

from sync_data.data.user_config import ConfigName
from sync_data.tool.douban import base
from sync_data.tool.douban.base import DouBanBase
from sync_data.tool.douban.data.enum_data import MediaInfo, MediaType, MediaStatus, Enum
from sync_data.tool.douban.soup import parser
from sync_data.tool.douban.soup.parser import ParserHtmlText
from sync_data.tool.douban.tmp import douban_books
from sync_data.tool.notion import databases
from sync_data.utils import log_detail
from sync_data.utils.config import Config


def add_cookies():
    # cookies_str = input('--------------------------\n'
    #                     '请输入你的豆瓣cookies(从ll=开始):')
    cookies_str = ''
    log_detail.info("【RUN】处理用户cookies")
    if cookies_str[0:3] == "ll=":
        cookies_dict = {}
        cookies_list = cookies_str.replace('"', "").split('; ')
        for i in cookies_list:
            name, value = i.split('=', 1)
            cookies_dict[f'{name}'] = value
        return cookies_dict
    else:
        log_detail.info("【RUN】你输入的cookies有无，请重新填写")
        # add_cookies()


def get_url_and_parser_to_inster_databases():

    config_dict = Config().get_config()
    user_id = config_dict[ConfigName.DOUBAN.value][ConfigName.DOUBAN_USER_ID.value]
    log_detail.info(f"【RUN】得到用户id：{user_id}")
    user_agent = config_dict[ConfigName.USER_AGENT.value]
    log_detail.info(f"【RUN】得到浏览器user-agent：{user_agent}")
    # 创建一个豆瓣实例
    douban_instance = base.DouBanBase(user_agent=user_agent)
    log_detail.debug("【RUN】创建一个豆瓣实例")

    wish_book_html = douban_instance.get_html_text(user_id=user_id,
                                                   media_type=MediaType.BOOK.value,
                                                   media_status=MediaStatus.WISH.value)
    log_detail.debug(f"【RUN】获取用户{user_id}的想读的书的页面")

    # 创建一个解析想读页面的实例
    wish_instance = parser.ParserHtmlText(wish_book_html)
    # TODO 解析出url

    # 遍历url
    url = "https://book.douban.com/subject/10554308/"
    # 得到详情页
    html_text = douban_instance.get_html_text(url=url,
                                              user_id=user_id,
                                              media_type=MediaType.BOOK.value,
                                              media_status=MediaStatus.WISH.value)
    # 创一个详情页实例
    html_parser = parser.ParserHtmlText(html_text=html_text)
    # 解析详情页，获取数据字典
    html_dict = html_parser.get_parser_dict(MediaType.BOOK.value)

    # 添加url
    html_dict[MediaInfo.URL.value] = url

    # 获取notion数据库id
    book_db_id = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_BOOK.value]
    # body = databases.get_notion_body(data_dict=html_dict, database_id=book_db_id)
    pages_id = databases.update_database(html_dict,
                                         book_db_id,
                                         config_dict[ConfigName.NOTION.value][ConfigName.NOTION_TOKEN.value])

    print(pages_id)


def test_url_list():
    # 初始化，获取配置信息
    config_dict = Config().get_config()

    # 获取浏览器user-agent
    user_agent = config_dict[ConfigName.USER_AGENT.value]
    log_detail.info(f"【RUN】得到浏览器user-agent：{user_agent}")

    # 获取豆瓣信息
    user_id = config_dict[ConfigName.DOUBAN.value][ConfigName.DOUBAN_USER_ID.value]
    log_detail.info(f"【RUN】得到用户id：{user_id}")

    # 获取notion信息
    book_db_id = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_BOOK.value]
    token = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_TOKEN.value]

    # 创建一个豆瓣实例
    douban_instance = base.DouBanBase(user_agent=user_agent)
    log_detail.debug("【RUN】创建一个豆瓣实例")
    # 获取html
    html_text = douban_instance.get_html_text(user_id=user_id)

    # 创建一个解析实例
    info_instance = ParserHtmlText(html_text)

    # 获取全部url
    url_list = info_instance.get_url_list()
    print(url_list)
    # 判断url的长度，小于15结束程序，大于15提取下一页
    for url in url_list:

        # 随机休眠5-10秒钟
        time_number = random.randint(5, 10)
        log_detail.info(f"【RUN】随机休眠时间5-10s，本次休眠：{time_number}s")

        html_text = douban_instance.get_html_text(url=url,
                                                  user_id=user_id,
                                                  media_type=MediaType.BOOK.value,
                                                  media_status=MediaStatus.WISH.value)
        # 创一个详情页实例
        html_parser = parser.ParserHtmlText(html_text=html_text)
        # 解析详情页，获取数据字典
        html_dict = html_parser.get_parser_dict(MediaType.BOOK.value)

        # 添加url
        html_dict[MediaInfo.URL.value] = url

        databases.update_database(data_dict=html_dict,
                                  database_id=book_db_id,
                                  token=token)

    log_detail.info("【RUN】完成数据库的导入！")


if __name__ == '__main__':
    # print("测试入口：")
    # get_url_and_parser_to_inster_databases()
    # notion_test()
    test_url_list()
    # log_detail.info("info")
    # log_detail.warn("warn")
