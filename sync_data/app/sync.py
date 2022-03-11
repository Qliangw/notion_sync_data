# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/3/4 14:45
# @Function:

import random

from sync_data.data.user_config import ConfigName
from sync_data.tool.douban import base
from sync_data.tool.douban.data.enum_data import MediaType, MediaStatus, MediaInfo
from sync_data.tool.douban.soup import parser
from sync_data.tool.douban.soup.parser import ParserHtmlText
from sync_data.tool.notion import databases
from sync_data.tool.notion.databases import create_database
from sync_data.tool.notion.query import get_notion_media_status
from sync_data.utils import log_detail
from sync_data.utils.config import Config, auto_config_database, get_auto_config, save_auto_config


def get_and_update(instance,
                   user_id,
                   media_type,
                   media_status,
                   start_number,
                   token,
                   database_id):
    """
    获取豆瓣信息 并 写入数据库

    :param instance:
    :param user_id:
    :param media_type:
    :param media_status:
    :param start_number:
    :param token:
    :param database_id:
    :return:
    """
    while True:
        page_number = int(start_number / 15 + 1)
        # 获取html
        html_text = instance.get_html_text(user_id=user_id,
                                           media_type=media_type,
                                           media_status=media_status,
                                           start_number=start_number)
        log_detail.info(f"【RUN】访问第{page_number}页数据完成")

        # 创建一个解析实例
        info_instance = ParserHtmlText(html_text)
        # 获取全部url
        url_list = info_instance.get_url_list()
        url_num = len(url_list)
        log_detail.info(f"【RUN】本页有{url_num}个媒体")
        for url in url_list:
            now_status = ""
            if media_status == MediaStatus.WISH.value:
                now_status = "想看"
            elif media_status == MediaStatus.DO.value:
                now_status = "在看"
            elif media_status == MediaStatus.COLLECT.value:
                now_status = "看过"
            # 查询数据库中是否存在
            notion_media_status = get_notion_media_status(token=token,
                                                          database_id=database_id,
                                                          media_url=url)
            if notion_media_status == "不存在":
                html_text = instance.get_html_text(url=url,
                                                   user_id=user_id,
                                                   media_type=media_type,
                                                   media_status=media_status)
                # 创一个详情页实例
                html_parser = parser.ParserHtmlText(html_text=html_text)
                # 解析详情页，获取数据字典
                html_dict = html_parser.get_parser_dict(media_type=media_type)

                # 添加url
                html_dict[MediaInfo.URL.value] = url

                databases.update_database(data_dict=html_dict,
                                          database_id=database_id,
                                          token=token,
                                          media_status=media_status,
                                          media_type=media_type)
                # 随机休眠5-10秒钟
                time_number = random.randint(5, 10)
                log_detail.info(f"【RUN】随机休眠时间5-10s，本次休眠：{time_number}s")

            elif notion_media_status != now_status:
                log_detail.warn("【RUN】豆瓣标记状态已经改变,notion状态同步功能暂不支持！")
            else:
                log_detail.info(f"【RUN】notion中含有本条数据，已跳过！媒体链接：{url}")
        log_detail.info(f"【RUN】完成第{page_number}页媒体数据库的导入！")
        print("*" * 15)
        if url_num > 14:
            start_number += 15
        else:
            break
    log_detail.info(f"【RUN】所有信息已导入notion，共计导入{(page_number - 1) * 15 + len(url_list)}条数据。")


def start_sync(media_type, media_status):
    # 初始化，获取配置信息
    config_dict = Config().get_config()

    # 获取浏览器user-agent
    user_agent = config_dict[ConfigName.USER_AGENT.value]
    log_detail.info(f"【RUN】得到浏览器user-agent：{user_agent}")

    # 获取豆瓣信息
    user_id = config_dict[ConfigName.DOUBAN.value][ConfigName.DOUBAN_USER_ID.value]
    log_detail.info(f"【RUN】得到用户id：{user_id}")

    # 获取notion数据库的信息
    token = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_TOKEN.value]
    auto_config = get_auto_config()
    database_id = ''
    if media_type == MediaType.BOOK.value:
        # database_id = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_BOOK.value]
        database_id = auto_config[ConfigName.NOTION_BOOK.value]
    elif media_type == MediaType.MUSIC.value:
        # database_id = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_MUSIC.value]
        database_id = auto_config[ConfigName.NOTION_MUSIC.value]
    elif media_type == MediaType.MOVIE.value:
        database_id = auto_config[ConfigName.NOTION_MOVIE.value]

    # 创建一个豆瓣实例
    douban_instance = base.DouBanBase(user_agent=user_agent)
    log_detail.debug("【RUN】创建一个豆瓣实例")

    # 从第0个媒体开始获取
    start_number = 0

    get_and_update(instance=douban_instance,
                   user_id=user_id,
                   media_type=media_type,
                   media_status=media_status,
                   start_number=start_number,
                   token=token,
                   database_id=database_id)


def init_database():
    """
    初始化数据库
    :return:
    """
    config_dict = Config().get_config()
    token = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_TOKEN.value]
    page_id = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_PAGE_ID.value]
    media_type_list = [MediaType.BOOK.value, MediaType.MUSIC.value, MediaType.MOVIE.value]

    #########################################################
    # 下个版本删除
    # book_db_id = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_BOOK.value]
    # tv_db_id = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_TV.value]
    # media_type = [MediaType.BOOK.value, MediaType.MUSIC.value, MediaType.MOVIE.value]
    try:
        auto_conf = get_auto_config()
        log_detail.info("【RUN】将个人数据库配置复制到auto.yaml中，将来版本会移除移动配置的功能！")
        if auto_conf[ConfigName.NOTION_BOOK.value] == "" or len(auto_conf[ConfigName.NOTION_BOOK.value]) != 32:
            book_db_id = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_BOOK.value]
            auto_conf[ConfigName.NOTION_BOOK.value] = book_db_id if len(book_db_id) == 32 else ""

        if auto_conf[ConfigName.NOTION_MUSIC.value] == "" or len(auto_conf[ConfigName.NOTION_MUSIC.value]) != 32:
            music_db_id = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_MUSIC.value]
            auto_conf[ConfigName.NOTION_MUSIC.value] = music_db_id if len(music_db_id) == 32 else ""

        if auto_conf[ConfigName.NOTION_MOVIE.value] == "" or len(auto_conf[ConfigName.NOTION_MOVIE.value]) != 32:
            movie_db_id = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_MOVIE.value]
            auto_conf[ConfigName.NOTION_MOVIE.value] = movie_db_id if len(movie_db_id) == 32 else ""

        save_auto_config(auto_conf)
    except Exception as err:
        log_detail.error(f"【RUN】config配置参数问题：{err}")
    #########################################################
    auto_config = get_auto_config()
    log_detail.debug(auto_config)
    # 书籍
    if auto_config[ConfigName.NOTION_BOOK.value] == "" or len(auto_config[ConfigName.NOTION_BOOK.value]) != 32:
        database_id = create_database(token=token, page_id=page_id, media_type=media_type_list[0])
        database_id = database_id.replace('-', '')
        r = auto_config_database(media_type=media_type_list[0], database_id=database_id)
        if r == 'succeed':
            log_detail.info(f"【RUN】初始化<{media_type_list[0]}>数据库完成！")
    else:
        log_detail.warn(f"【RUN】<{media_type_list[0]}>数据库已存在，跳过初始化！")

    # 音乐
    if auto_config[ConfigName.NOTION_MUSIC.value] == "" or len(auto_config[ConfigName.NOTION_MUSIC.value]) != 32:
        database_id = create_database(token=token, page_id=page_id, media_type=media_type_list[1])
        database_id = database_id.replace('-', '')
        r = auto_config_database(media_type=media_type_list[1], database_id=database_id)
        if r == 'succeed':
            log_detail.info(f"【RUN】初始化<{media_type_list[1]}>数据库完成！")
    else:
        log_detail.warn(f"【RUN】<{media_type_list[1]}>数据库已存在，跳过初始化！")

    # 影视
    if auto_config[ConfigName.NOTION_MOVIE.value] == "" or len(auto_config[ConfigName.NOTION_MOVIE.value]) != 32:
        # log_detail.info(f"【RUN】暂不支持<{media_type_list[2]}>数据库的初始化")
        # return 0
        database_id = create_database(token=token, page_id=page_id, media_type=media_type_list[2])
        database_id = database_id.replace('-', '')
        r = auto_config_database(media_type=media_type_list[2], database_id=database_id)
        if r == 'succeed':
            log_detail.info(f"【RUN】初始化<{media_type_list[2]}>数据库完成！")
    else:
        log_detail.warn(f"【RUN】<{media_type_list[2]}>数据库已存在，跳过初始化！")
