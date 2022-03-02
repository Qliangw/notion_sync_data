# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/2/27 21:29
# @Function: notion 数据库处理

import json
from sync_data.utils import log_detail
from sync_data.tool.notion import base
from sync_data.utils.http_utils import RequestUtils

# TODO 添加书 影 音 数据库


def create_database(token, page_id):
    """
    创建新的数据库
    :param token: notion->setting->integrations->develop your own integrations
    :param page_id: 浏览器打开notion，链接的尾部获取
    :return: databases_id，可以通过该id定位到数据库
    """
    db_data = base.NotionBaseInfo(token=token)
    log_detail.info("【RNU】创建数据库--初始化参数")
    create_db_data = {
        "parent": {"type": "page_id", "page_id": f"{page_id}"},
        "title": [{"type": "text", "text": {"content": "豆瓣书单库"}}],
        "icon": {"type": "emoji", "emoji": "📚"},
        "properties": {
            "书名": {"title": {}},
            "评分": {"select": {"options": [
                {"name": "⭐", "color": "yellow"},
                {"name": "⭐⭐", "color": "yellow"},
                {"name": "⭐⭐⭐", "color": "yellow"},
                {"name": "⭐⭐⭐⭐", "color": "yellow"},
                {"name": "⭐⭐⭐⭐⭐", "color": "yellow"}]}},
            "短评": {"rich_text": {}},
            "标记时间": {"date": {}},
            "豆瓣链接": {"url": {}},
            "作者": {"multi_select": {}},
            "类型": {"multi_select": {}},
            "出版社": {"multi_select": {}},
            "ISBN": {"url": {}},
            "封面": {"files": []},
            "出版年份": {"select": {}},
            "标记状态": {"select": {}}}}

    params = json.dumps(create_db_data)
    # print(params)
    log_detail.info("【RNU】创建数据库--post请求")
    # res = RequestUtils.post(url=db_data.get_db_url(), params=params, headers=db_data.get_headers())
    db_res = RequestUtils()
    res = db_res.post(url=db_data.get_db_url(), params=params, headers=db_data.get_headers())
    if res.status_code == 200:
        log_detail.info(res.text)
        database_id = eval(res.text.replace(":null", ":'null'").replace(":false", ":'false'"))["id"]
        return database_id
    else:
        log_detail.info("【Err】创建数据库失败，请检查是否页面有授权给【集权】，再重新使用本程序")
        input("请按Enter键结束！")
        exit()

