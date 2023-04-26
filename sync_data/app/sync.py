# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/3/4 14:45
# @Function:

import random
import os

from sync_data.data.user_config import ConfigName, get_desensitization_of_user_info
from sync_data.tool.douban import base
from sync_data.tool.douban.data.enum_data import MediaType, MediaStatus, MediaInfo
from sync_data.tool.douban.soup import parser
from sync_data.tool.douban.soup.parser import ParserHtmlText
from sync_data.tool.notion import databases
from sync_data.tool.notion.databases import create_database
from sync_data.tool.notion.query import get_notion_media_status
from sync_data.utils import log_detail
from sync_data.utils.config import Config


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
    # 解析出错的url
    parser_err_url_list = []
    # 导入notion出错的url
    update_err_url_list = []

    jump_number = 0
    page_monitoring_number = 0
    page_jump_number = 0

    while True:
        page_number = int(start_number / 15 + 1)
        # 获取html
        html_text = instance.get_html_text(user_id=user_id,
                                           media_type=media_type,
                                           media_status=media_status,
                                           start_number=start_number)
        log_detail.info(f"【DouBan】访问{media_type}中标记为{media_status}的状态第{page_number}页数据完成")

        # 创建一个解析实例
        info_instance = ParserHtmlText(html_text)
        # 获取全部url TODO 获取标记时间->主要针对书籍
        url_dict = info_instance.get_url_dict(monitoring_day=monitoring_day, media_type=media_type)
        url_list = url_dict["url_list"]
        log_detail.debug(f"【DouBan】- 获取本页所有{media_type}的链接")

        # 记录for循环次数，即解析url的次数
        count_num = 0
        url_num = len(url_list)
        monitoring_info = url_dict["monitoring_info"]
        log_detail.info(f"【DouBan】- 第{page_number}页共有媒体个数：{url_num}")
        log_detail.info(f"【DouBan】- 第{page_number}页监控日期内数据个数：{monitoring_info[0]}")
        log_detail.info(f"【DouBan】- 是否继续访问下一页：{monitoring_info[1]}")

        update_err_number = 0
        parser_err_number = 0
        # 解析该页媒体的每个url
        for url in url_list:

            if count_num == monitoring_info[0] and monitoring_info[1] is False:
                log_detail.info("【DouBan】- 其他媒体不在监控时间内，结束导入")
                # 如果循环次数等于监控日期内媒体的个数，且不访问下一页时，退去本次循环
                break
            else:
                count_num += 1
                log_detail.debug(f"【DouBan】--解析url的次数：{count_num}")

            # 当前媒体标记状态
            now_status = ""
            if media_status == MediaStatus.WISH.value and media_type != MediaType.GAME.value:
                now_status = "想看"
            elif media_status == MediaStatus.DO.value and media_type != MediaType.GAME.value:
                now_status = "在看"
            elif media_status == MediaStatus.COLLECT.value and media_type != MediaType.GAME.value:
                now_status = "看过"
            elif media_status == MediaStatus.WISH.value and media_type == MediaType.GAME.value:
                now_status = "想玩"
            elif media_status == MediaStatus.DO.value and media_type == MediaType.GAME.value:
                now_status = "在玩"
            elif media_status == MediaStatus.COLLECT.value and media_type == MediaType.GAME.value:
                now_status = "玩过"

            # 查询数据库中是否存在该媒体，通过检索url唯一值
            notion_media_status, old_data_json = get_notion_media_status(token=token,
                                                                         database_id=database_id,
                                                                         media_url=url)
            # 随机休眠0-1秒钟，访问notion（应该可以不用延迟，还没有细看notion接口）
            time_number = random.random()
            log_detail.debug(f"【RUN】- notion随机访问休眠时间0-1s，本次休眠：{time_number}s")

            # 如果数据库中不存在，则开始解析豆瓣媒体详情页
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
                        html_dict[MediaInfo.MY_DATE.value] = url_dict['mark_date'][count_num-1]
                    else:
                        log_detail.warn(f"【RUN】- 解析该页面出现问题，媒体链接：{url}")
                        parser_err_url_list.append(url)
                        parser_err_number += 1
                        continue

                    opt_status = databases.get_flag_update_database(data_dict=html_dict,
                                                                    database_id=database_id,
                                                                    token=token,
                                                                    media_status=media_status,
                                                                    media_type=media_type)
                    if opt_status == "succeed":
                        log_detail.info(f'【RUN】- 导入《{html_dict[MediaInfo.TITLE.value]}》成功。媒体链接：{url}')
                    elif opt_status == "failed":
                        update_err_url_list.append(url)
                        update_err_number += 1
                        log_detail.warn(f'【RUN】- 导入《{html_dict[MediaInfo.TITLE.value]}》失败！媒体链接：{url}')
                    elif opt_status == "exception":
                        update_err_url_list.append(url)
                        log_detail.error(f'【RUN】捉到Bug了,请您反馈！')

                    # 随机休眠5-10秒钟
                    time_number = random.randint(1, 10)
                    log_detail.info(f"【RUN】- 访问豆瓣时随机休眠时间1-10s，本次休眠：{time_number}s")
                else:
                    log_detail.warn(f"【RUN】- 访问该页面出现问题，媒体链接：{url}")
                    parser_err_url_list.append(url)
            # 如果数据库中存在，则判断标记状态是否相同，不同则更新
            elif notion_media_status != now_status:
                log_detail.info("【RUN】豆瓣标记状态已经改变，更新数据")
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
                        parser_err_url_list.append(url)
                        parser_err_number += 1
                        continue
                    page_id = old_data_json['results'][0]['id']
                    opt_status = databases.get_flag_update_old_database(data_dict=html_dict,
                                                                        page_id=page_id,
                                                                        token=token,
                                                                        media_status=media_status,
                                                                        media_type=media_type)
                    if opt_status == "succeed":
                        log_detail.info(f'【RUN】- 更新《{html_dict[MediaInfo.TITLE.value]}》成功。媒体链接：{url}')
                    elif opt_status == "failed":
                        update_err_url_list.append(url)
                        update_err_number += 1
                        log_detail.warn(f'【RUN】- 更新《{html_dict[MediaInfo.TITLE.value]}》失败！媒体链接：{url}')
                    elif opt_status == "exception":
                        update_err_url_list.append(url)
                        log_detail.error(f'【RUN】捉到Bug了,请您反馈！')
                    # 随机休眠5-10秒钟
                    time_number = random.randint(1, 10)
                    log_detail.info(f"【RUN】- 访问豆瓣时随机休眠时间1-10s，本次休眠：{time_number}s")
                else:
                    log_detail.warn(f"【RUN】- 访问该页面出现问题，媒体链接：{url}")
                    parser_err_url_list.append(url)
            else:
                # 随机休眠0-1秒钟，访问notion（应该可以不用延迟，还没有细看notion接口）
                time_number = random.random()
                log_detail.debug(f"【RUN】- notion随机访问休眠时间0-1s，本次休眠：{time_number}s")

                jump_number += 1
                log_detail.info(f"【RUN】notion中含有本条数据，已跳过！媒体链接：{url}")

        log_detail.info(f"【RUN】完成第{page_number}页媒体数据库的导入！")
        log_detail.info(f"【RUN】 - 第{page_number}页监控数据个数：{monitoring_info[0]}")
        log_detail.info(f"【RUN】 - 第{page_number}页跳过数据个数：{jump_number}")
        log_detail.info(f"【RUN】 - 第{page_number}页解析失败个数：{parser_err_number}")
        log_detail.info(f"【RUN】 - 第{page_number}页导入失败个数：{update_err_number}")
        page_monitoring_number += int(monitoring_info[0])
        page_jump_number += int(jump_number)
        jump_number = 0

        log_detail.info("--------------------------------------------------")
        if monitoring_info[1] is False:
            break
        if url_num > 13:
            # 翻页处理
            start_number += 15
        else:
            break

    # print(monitoring_info)
    log_detail.info(f"【RUN】您的标记 <{media_status}> 状态的 <{media_type}> 已导入notion")
    log_detail.info(f"【RUN】 - 共计访问页数：{page_number}")
    log_detail.info(f"【RUN】 -- 访问数据个数：{(page_number - 1) * 15 + len(url_list)}")
    log_detail.info(f"【RUN】 -- 监控数据个数：{page_monitoring_number}")
    log_detail.info(f"【RUN】 -- 跳过数据个数：{page_jump_number}")
    # log_detail.info(f"【RUN】 -- 修改数据个数：{page_monitoring_number - page_jump_number}")
    log_detail.info(f"【RUN】 -- 导入数据个数：{page_monitoring_number - page_jump_number}")

    # 如果存在解析失败的媒体，则打印出媒体链接
    log_detail.info(f"【RUN】 -- 解析失败个数：{len(parser_err_url_list)}")
    if parser_err_url_list:
        for i in range(0, len(parser_err_url_list)):
            log_detail.info(f"【RUN】 --- 第{i + 1}个媒体链接：{parser_err_url_list[i]}")

    # 如果存在导入失败的媒体，则打印出媒体链接
    log_detail.info(f"【RUN】 -- 导入失败个数：{len(update_err_url_list)}")
    if update_err_url_list:
        for i in range(0, len(update_err_url_list)):
            log_detail.info(f"【RUN】 --- 第{i + 1}个媒体链接：{update_err_url_list[i]}")

    return parser_err_url_list


def start_sync(media_type, media_status):
    # 初始化，获取配置信息
    config_dict = Config().get_config()
    log_detail.info("【Config】读取用户配置的文件[config.yaml]")

    # 获取浏览器user-agent
    user_agent = config_dict[ConfigName.USER_AGENT.value] or os.environ["USER_AGENT"]
    user_cookie = config_dict[ConfigName.DOUBAN.value][ConfigName.USER_COOKIE.value] or os.environ["USER_COOKIE"]
    log_detail.info(f"【Config】- 取得浏览器 user-agent：{user_agent}")

    # 获取豆瓣信息
    user_id = config_dict[ConfigName.DOUBAN.value][ConfigName.DOUBAN_USER_ID.value] or os.environ["DOUBAN_USER_ID"]
    # 用户id脱敏处理
    x_user_id = get_desensitization_of_user_info(user_id)
    log_detail.info(f"【Config】- 取得用户 id：{x_user_id}")
    monitoring_day = config_dict[ConfigName.DOUBAN.value][ConfigName.DOUBAN_DAY.value] or int(os.environ["DOUBAN_DAY"])
    log_detail.info(f"【Config】- 取得监控日期：{monitoring_day}")

    # 获取notion数据库的信息
    token = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_TOKEN.value] or os.environ["NOTION_TOKEN"]
    x_token = get_desensitization_of_user_info(token)
    log_detail.info(f"【Config】- 取得 notion 的 token：{x_token}")

    # auto_config = Config().get_config()
    database_id = ''
    if media_type == MediaType.BOOK.value:
        database_id = config_dict['notion'][ConfigName.NOTION_BOOK.value] or os.environ["NOTION_BOOKS_DB"]
    elif media_type == MediaType.MUSIC.value:
        database_id = config_dict['notion'][ConfigName.NOTION_MUSIC.value] or os.environ["NOTION_MUSIC_DB"]
    elif media_type == MediaType.MOVIE.value:
        database_id = config_dict['notion'][ConfigName.NOTION_MOVIE.value] or os.environ["NOTION_MOVIE_DB"]
    elif media_type == MediaType.GAME.value:
        database_id = config_dict['notion'][ConfigName.NOTION_GAME.value] or os.environ["NOTION_GAME_DB"]
    try:
        if database_id is None:
            log_detail.info(f"【Config】配置文件缺少重要参数")
            return None

        # 加密显示
        x_database_id = get_desensitization_of_user_info(database_id)
        log_detail.info(f"【Notion】- 取得notion的database_id：{x_database_id}")
        # 创建一个豆瓣实例
        douban_instance = base.DouBanBase(user_agent=user_agent, user_cookies=user_cookie)
        log_detail.debug("【DouBan】创建一个豆瓣实例")

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
    except Exception as err:
        log_detail.info(f"【ERROR】start_sync:{err}")





def init_database():
    """
    初始化数据库
    :return:
    """
    config_dict = Config().get_config()
    log_detail.info("【Config】读取用户配置的文件[config.yaml]")
    token = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_TOKEN.value]
    x_token = get_desensitization_of_user_info(token)
    log_detail.info(f"【Notion】- 取得 notion 的 token：{x_token}")
    page_id = config_dict[ConfigName.NOTION.value][ConfigName.NOTION_PAGE_ID.value]
    x_page_id = get_desensitization_of_user_info(page_id)
    log_detail.info(f"【Notion】- 取得 notion 的 page_id：{x_page_id}")

    log_detail.info("【Notion】开始notion对应豆瓣书影音的初始化...")
    init_simple_database(config_dict=config_dict, media_type=MediaType.BOOK.value, token=token, page_id=page_id)
    init_simple_database(config_dict=config_dict, media_type=MediaType.MOVIE.value, token=token, page_id=page_id)
    init_simple_database(config_dict=config_dict, media_type=MediaType.MUSIC.value, token=token, page_id=page_id)
    init_simple_database(config_dict=config_dict, media_type=MediaType.GAME.value, token=token, page_id=page_id)
    log_detail.info("【Notion】数据库初始化完成。")
    log_detail.info(
        "【Tip】已在notion页面创建数据库，请输入<python run.py -m [book/music/movie/game] -s [wish/do/collect/all]>完成媒体的导入")


def init_simple_database(config_dict, media_type, token, page_id):
    """
    初始化单个数据库

    :param config_dict: 配置内容,字典格式
    :param media_type: 媒体类型
    :param token: token
    :param page_id: 页面id
    :return: None
    """
    try:
        # 配置notion数据库id
        if config_dict['notion'][f'{media_type}_database_id'] is None or config_dict['notion'][f'{media_type}_database_id'] == '':
            database_id = create_database(token=token, media_type=media_type, page_id=page_id)
            database_id = database_id.replace('-', '')

            config_dict['notion'][f'{media_type}_database_id'] = database_id

            Config().save_config(config_dict)

            log_detail.info(f"【Notion】- 初始化<{media_type}> 数据库完成。")
        else:
            log_detail.info(f"【Notion】- <{media_type}> 数据库已存在，跳过初始化！")
    except Exception as err:
        log_detail.error(f"【Notion】- 尝试创建<{media_type}> 数据库时失败。错误：{err}")


def merge_old_cfg():
    old_cfg = Config().get_auto_config()
    _cfg = Config().get_config()
    try:
        if old_cfg is None:
            log_detail.info("【Config】旧配置为空，退出合并程序")
        else:
            old_cfg_keys = list(old_cfg.keys())
            for i in old_cfg_keys:
                if old_cfg[i] is None:
                    log_detail.info(f"【Config】旧配置{i}不存在")
                else:
                    _cfg['notion'][i] = old_cfg[i]
                    log_detail.info(f"【Config】合并{i}成功")
        Config().save_config(_cfg)
        log_detail.info(f"【Config】旧配置已合并至[config.yaml]")
    except Exception as err:
        log_detail.error(f"【Config】合并旧配置时出错：{err}")
