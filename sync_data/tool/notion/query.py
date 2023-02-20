# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/3/5 10:05
# @Function:


import json

from sync_data.tool.notion.base import NotionBaseInfo
from sync_data.utils import log_detail
from sync_data.utils.http_utils import RequestUtils


def query_db_data(token, database_id, media_url):
    """
    查询数据库的数据

    :param database_id: notion数据库id
    :param media_url: 数据库的索引--豆瓣媒体的url
    :param token: token
    :return: json格式的数据，参考notion官方api
    """
    base = NotionBaseInfo(token=token)
    api_url = base.get_db_url()
    api_url = f"{api_url}/{database_id}/query"
    params = json.dumps({
        "filter": {
            "property": "豆瓣链接",
            "url": {
                "equals": f"{media_url}"
            }
        }
    })
    headers = base.get_headers()
    req = RequestUtils()
    res = req.post(url=api_url, headers=headers, params=params)
    return res.json()


def get_notion_media_status(token, database_id, media_url):
    """
    查询数据库中媒体url的标记状态

    :param token:
    :param database_id:
    :param media_url:
    :return: 媒体标记状态：【想看、看过、已看】不存在
    """
    data_json = query_db_data(token=token, database_id=database_id, media_url=media_url)
    # print(data_json['results'])
    if not data_json['results']:
        return "不存在", data_json
    else:
        notion_media_status = data_json['results'][0]['properties']['标记状态']['select']['name']
        log_detail.debug(f"【RUN】- 数据库中的状态为：{notion_media_status}")
        return notion_media_status, data_json
