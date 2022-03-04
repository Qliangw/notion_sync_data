# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/2/27 21:29
# @Function: notion 数据库处理

import json
import re

import requests

from sync_data.tool.douban.data.enum_data import MediaInfo, MediaStatus
from sync_data.utils import log_detail
from sync_data.tool.notion import base
from sync_data.utils.http_utils import RequestUtils


def get_book_body(data_dict, database_id, media_status):
    """
    获取json数据

    :param media_status:
    :param data_dict:
    :param database_id:
    :return:
    """
    if media_status == MediaStatus.WISH.value:
        media_status = "想看"
    elif media_status == MediaStatus.DO.value:
        media_status = "在看"
    elif media_status == MediaStatus.COLLECT.value:
        media_status = "看过"
    else:
        media_status = ""

    log_detail.info("【RUN】数据信息整理为json格式")
    body = {
        "parent": {
            "type": "database_id",
            "database_id": f"{database_id}"
        },
        "properties": {
            "书名": {
                "title": [{
                    "type": "text",
                    "text": {
                        "content": data_dict[MediaInfo.TITLE.value]
                    }
                }]
            },
            "ISBN": {
                "url": f"https://isbnsearch.org/isbn/{data_dict[MediaInfo.ISBN.value]}"
            },
            "封面": {
                "files": [{
                    "type": "external",
                    "name": data_dict[MediaInfo.IMG.value][-13:],
                    "external": {
                        "url": data_dict[MediaInfo.IMG.value]
                    }
                }]
            },
            "评分": {
                "number": float(data_dict[MediaInfo.RATING_F.value])
            },
            "作者": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": data_dict[MediaInfo.AUTHOR.value]
                    }
                }]
            },
            "出版年份": {
                "select": {
                    "name": data_dict[MediaInfo.PUB_DATE.value][0:4]
                }
            },
            "出版社": {
                "select": {
                    "name": data_dict[MediaInfo.PUBLISHER.value]
                }
            },
            "价格": {
                "number": float(data_dict[MediaInfo.PRICE.value])
            },
            "评分人数": {
                "number": int(data_dict[MediaInfo.ASSESS.value])
            },
            "页数": {
                "number": int(data_dict[MediaInfo.PAGES.value])
            },
            "标记状态": {
                "select": {
                    "name": f"{media_status}"
                }
            },
            "豆瓣链接": {
                "url": f"{data_dict[MediaInfo.URL.value]}"
            }
        }
    }
    return body


def create_database(token, page_id):
    """
    创建新的数据库
    :param token: notion->setting->integrations->develop your own integrations
    :param page_id: 浏览器打开notion，链接的尾部获取
    :return: databases_id，可以通过该id定位到数据库
    """
    # TODO 添加书 影 音 数据库
    db_data = base.NotionBaseInfo(token=token)
    log_detail.info("【RNU】创建数据库--初始化参数")
    create_db_data = {
        "parent": {"type": "page_id", "page_id": f"{page_id}"},
        "title": [{"type": "text", "text": {"content": "豆瓣书单库"}}],
        "icon": {"type": "emoji", "emoji": "📚"},
        "properties": {
            "书名": {"title": {}},
            "评分": {"number": {}},
            "豆瓣链接": {"url": {}},
            "作者": {"rich_text": {}},
            "出版社": {"select": {}},
            "ISBN": {"url": {}},
            "封面": {"files": []},
            "出版年份": {"select": {}},
            "价格": {"number": {}},
            "评分人数": {"number": {}},
            "页数": {"number": {}},
            "短评": {"rich_text": {}},
            "类型": {"multi_select": {}},
            "标记状态": {"select": {}},
            "标记时间": {"date": {}},
            "个人评分": {"select": {"options": [
                {"name": "⭐", "color": "yellow"},
                {"name": "⭐⭐", "color": "yellow"},
                {"name": "⭐⭐⭐", "color": "yellow"},
                {"name": "⭐⭐⭐⭐", "color": "yellow"},
                {"name": "⭐⭐⭐⭐⭐", "color": "yellow"}]}},
        }}

    params = json.dumps(create_db_data)
    # print(params)
    log_detail.debug("【RNU】创建数据库--post请求")
    # res = RequestUtils.post(url=db_data.get_db_url(), params=params, headers=db_data.get_headers())
    db_res = RequestUtils()
    res = db_res.post(url=db_data.get_db_url(), params=params, headers=db_data.get_headers())
    if res.status_code == 200:
        log_detail.info(res.text)
        database_id = eval(res.text.replace(":null", ":'null'").replace(":false", ":'false'"))["id"]
        return database_id
    else:
        log_detail.warn("【RUN】创建数据库失败，请检查是否页面有授权给【集权】，再重新使用本程序")
        input("请按Enter键结束！")
        exit()


def update_database(data_dict, database_id, token):
    """
    写入数据库

    :param data_dict: 待写入数据字典
    :param database_id: 数据库id
    :param token:【必须】
    :return: TODO 返回一个成功后的页面ID
    """
    try:
        body = get_book_body(data_dict, database_id, MediaStatus.WISH.value)
        body = json.dumps(body)
        page_data = base.NotionBaseInfo(token)
        req = RequestUtils()
        res = req.post(url=page_data.get_page_url(),
                       headers=page_data.get_headers(),
                       params=body)
        if res.status_code == 200:
            log_detail.info(f"【RUN】导入《{data_dict[MediaInfo.TITLE.value]}》成功")
            return None
    except Exception as err:
        log_detail.error(f"【RUN】{err}")
        return None


