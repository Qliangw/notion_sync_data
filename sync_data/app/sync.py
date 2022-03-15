# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/3/4 14:45
# @Function:

import random

from sync_data.data.user_config import ConfigName, get_desensitization_of_user_info
from sync_data.tool.douban import base
from sync_data.tool.douban.data.enum_data import MediaType, MediaStatus, MediaInfo
from sync_data.tool.douban.soup import parser
from sync_data.tool.douban.soup.parser import ParserHtmlText
from sync_data.tool.notion import databases
from sync_data.tool.notion.databases import create_database
from sync_data.tool.notion.query import get_notion_media_status
from sync_data.utils import log_detail
from sync_data.utils.config import Config, auto_config_database, get_auto_config, save_auto_config


def get_monitoring_and_update(instance,
                              user_id,
                              monitoring_day,
                              media_type,
                              media_status,
                              start_number,
                              token,
                              database_id):
    """
    获取豆瓣信息 并 写入数据库

    :param instance: 豆瓣实例
    :param monitoring_day: 监控时间
    :param user_id: 豆瓣id
    :param media_type: 媒体类型
    :param media_status: 媒体状态
    :param start_number: 开始页数
    :param token: notion的token
    :param database_id: notion的数据库id
    :return:
    """
    err_url = []
    jump_number = 0
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
        url_dict = info_instance.get_url_dict(monitoring_day=monitoring_day)

        url_list = url_dict["url_list"]
        monitoring_info = url_dict["monitoring_info"]
        log_detail.info(f"【RUN】- 本页监控日期内的数据为：{monitoring_info[0]}")
        log_detail.info(f"【RUN】- 是否继续访问下一页：{monitoring_info[1]}")

        count_num = 0
        url_num = len(url_list)
        log_detail.info(f"【RUN】- 本页有{url_num}个媒体")
        for url in url_list:
            if count_num == monitoring_info[0] and monitoring_info[1] is False:
                log_detail.info("【RUN】- 其他媒体不在监控时间内，结束导入")
                break
            else:
                count_num += 1
                log_detail.debug(f"访问了{count_num}次，数组长度为{len(url_list)}")
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
            # 随机休眠0-1秒钟
            time_number = random.random()
            log_detail.debug(f"【RUN】- notion随机访问休眠时间0-1s，本次休眠：{time_number}s")
            if notion_media_status == "不存在":
                html_text = instance.get_html_text(url=url,
                                                   user_id=user_id,
                                                   media_type=media_type,
                                                   media_status=media_status)
                if html_text:
                    # 创一个详情页实例
                    html_parser = parser.ParserHtmlText(html_text=html_text)
                    # 解析详情页，获取数据字典
                    html_dict = html_parser.get_parser_dict(media_type=media_type)

                    # 添加url
                    if html_dict:
                        html_dict[MediaInfo.URL.value] = url
                    else:
                        log_detail.warn(f"【RUN】- 解析该页面出现问题，媒体链接：{url}")
                        err_url.append(url)
                        continue

                    databases.update_database(data_dict=html_dict,
                                              database_id=database_id,
                                              token=token,
                                              media_status=media_status,
                                              media_type=media_type)
                    # 随机休眠5-10秒钟
                    time_number = random.randint(1, 10)
                    log_detail.info(f"【RUN】访问豆瓣时随机休眠时间1-10s，本次休眠：{time_number}s")
                else:
                    log_detail.warn(f"【RUN】访问该页面出现问题，媒体链接：{url}")
                    err_url.append(url)
                    continue

            elif notion_media_status != now_status:
                log_detail.warn("【RUN】豆瓣标记状态已经改变,notion状态同步功能暂不支持！")
            else:
                log_detail.info(f"【RUN】notion中含有本条数据，已跳过！媒体链接：{url}")
                jump_number += 1
        log_detail.info(f"【RUN】完成第{page_number}页媒体数据库的导入！")
        print("*" * 15)
        if monitoring_info[1] is False:
            break
        if url_num > 14:
            start_number += 15
        else:
            break

    log_detail.info(f"【RUN】您的标记为 <{media_status}> 的 <{media_type}> 已导入notion")
    log_detail.info(f"【RUN】 - 共计{(page_number - 1) * 15 + len(url_list)}条数据。")
    log_detail.info(f"【RUN】 - 跳过{jump_number}条数据。")
    log_detail.info(f"【RUN】 - 失败{len(err_url)}条数据！")
    if err_url:
        for i in range(0, len(err_url)):
            log_detail.info(f"【RUN】--第{i}条失败的媒体链接为：{err_url[i]}")
    return err_url



def start_sync(media_type, media_status):
    # 初始化，获取配置信息
    config_dict = Config().get_config()
    log_detail.info("【RUN】读取用户配置的文件[config.yaml]")

    # 获取浏览器user-agent
    user_agent = config_dict[ConfigName.USER_AGENT.value]
    log_detail.info(f"【RUN】- 取得浏览器 user-agent：{user_agent}")

    # 获取豆瓣信息
    user_id = config_dict[ConfigName.DOUBAN.value][ConfigName.DOUBAN_USER_ID.value]
    # 用户id脱敏处理
    x_user_id = get_desensitization_of_user_info(user_id)
    log_detail.info(f"【RUN】- 取得用户 id：{x_user_id}")
    monitoring_day = config_dict[ConfigName.DOUBAN.value][ConfigName.DOUBAN_DAY.value]
    log_detail.info(f"【RUN】- 取得监控日期：{monitoring_day}")

    # 获取notion数据库的信息
    token = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_TOKEN.value]
    x_token = get_desensitization_of_user_info(token)
    log_detail.info(f"【RUN】- 取得 notion 的 token：{x_token}")

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
    x_database_id = get_desensitization_of_user_info(database_id)
    log_detail.info(f"【RUN】- 取得notion的database_id：{x_database_id}")

    # 创建一个豆瓣实例
    douban_instance = base.DouBanBase(user_agent=user_agent)
    log_detail.debug("【RUN】创建一个豆瓣实例")

    # 从第0个媒体开始获取
    start_number = 0
    err_url_list = get_monitoring_and_update(instance=douban_instance,
                                             monitoring_day=monitoring_day,
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
    log_detail.info("【RUN】读取用户配置的文件[config.yaml]")
    token = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_TOKEN.value]
    x_token = get_desensitization_of_user_info(token)
    log_detail.info(f"【RUN】- 取得 notion 的 token：{x_token}")
    page_id = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_PAGE_ID.value]
    page_id = get_desensitization_of_user_info(page_id)
    log_detail.info(f"【RUN】- 取得 notion 的 page_id：{page_id}")

    auto_config = get_auto_config()
    log_detail.debug(auto_config)
    log_detail.info("【RUN】开始notion对应豆瓣书影音的初始化...")
    init_simple_database(config=auto_config, media_type=ConfigName.NOTION_BOOK.value, token=token, page_id=page_id)
    init_simple_database(config=auto_config, media_type=ConfigName.NOTION_MOVIE.value, token=token, page_id=page_id)
    init_simple_database(config=auto_config, media_type=ConfigName.NOTION_MUSIC.value, token=token, page_id=page_id)
    log_detail.info("【RUN】数据库初始化完成。")
    log_detail.info("【Tip】已在notion页面创建数据库，请输入<python run.py -m [book/music/movie] -s [wish/do/collect/all]>完成媒体的导入")

def init_simple_database(config, media_type, token, page_id):
    try:
        if config[media_type] == "" or len(config[media_type]) != 32:
            database_id = create_database(token=token, media_type=media_type, page_id=page_id)
            database_id = database_id.replace('-', '')
            r = auto_config_database(media_type=media_type, database_id=database_id)
            if r == "succeed":
                log_detail.info(f"【RUN】- 初始化<{media_type}> 数据库完成。")
        else:
            log_detail.info(f"【RUN】- <{media_type}> 数据库已存在，跳过初始化！")
    except Exception as err:
        log_detail.error(f"【RUN】- 尝试创建<{media_type}> 数据库时失败。错误：{err}")