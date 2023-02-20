# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/2/27 21:29
# @Function: notion 数据库处理

import json
from datetime import datetime

from sync_data.tool.douban.data.enum_data import MediaInfo, MediaStatus, MediaType
from sync_data.tool.notion import base
from sync_data.tool.notion.data.enum_data import DatabaseProperty
from sync_data.utils import log_detail
from sync_data.utils.http_utils import RequestUtils


def get_multi_select_body(data_list):
    str_key = '{"name": "xxx"}'
    new_list_tmp = []
    for i in data_list:
        new_tmp = str_key.replace('xxx', i)
        new_list_tmp.append(new_tmp)
    # print(new_list_tmp)
    str_new = ','.join(new_list_tmp)
    return "[" + str_new + "]"


def get_non_null_params_body(property_type, property_params):
    """
    获取非空的body

    :param body_dict:
    :param property_name: 数据库属性名字
    :param property_type: 数据库属性类型
    :param property_params: 数据库要传入的参数
    :return: 字典类型的body
    """
    body_dict = {}
    if property_params:
        if property_type == DatabaseProperty.NUMBER.value:
            body_dict.update(number=property_params)
        elif property_type == DatabaseProperty.URL.value:
            body_dict.update(url=f"https://isbnsearch.org/isbn/{property_params}")
        elif property_type == DatabaseProperty.SELECT.value:
            tmp_dict = {}
            tmp_dict.update(name=property_params)
            body_dict.update(select=tmp_dict)
            # body_dict["select"].update(name=property_params)
        elif property_type == DatabaseProperty.DATE.value:
            date_obj = datetime.strptime(property_params, '%Y-%m-%d')
            iso_date_str = date_obj.date().isoformat()
            log_detail.debug(f"【RUN】- {property_params}转换为{iso_date_str}")
            tmp_dict = {}
            tmp_dict.update(start=iso_date_str)
            body_dict.update(date=tmp_dict)
        return body_dict
    else:
        return body_dict


def get_body(data_dict, database_id, media_status, media_type):
    """
    获取json数据

    :param media_type:
    :param media_status:
    :param data_dict:
    :param database_id:
    :return:
    """
    music_status, status, game_status = get_media_status(media_status)

    log_detail.info(f"【RUN】- {media_type}数据信息整理为json格式")
    rating = data_dict[MediaInfo.RATING_F.value]
    # rating = float(rat) if rat == "" else 0
    if media_type == MediaType.MUSIC.value:
        body = {
            "parent": {
                "type": "database_id",
                "database_id": f"{database_id}"
            },
            "properties": {
                "音乐": {
                    "title": [{
                        "type": "text",
                        "text": {
                            "content": data_dict[MediaInfo.TITLE.value]
                        }
                    }]
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
                "表演者": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": data_dict[MediaInfo.PERFORMER.value]
                        }
                    }]
                },
                "发行时间": {
                    "select": {
                        "name": data_dict[MediaInfo.RELEASE_DATE.value][0:4]
                    }
                },
                "标记状态": {
                    "select": {
                        "name": f"{music_status}"
                    }
                },
                "豆瓣链接": {
                    "url": f"{data_dict[MediaInfo.URL.value]}"
                }
            }
        }
        # 评分
        if data_dict[MediaInfo.RATING_F.value]:
            rating_f = float(data_dict[MediaInfo.RATING_F.value])
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.NUMBER.value,
                                                property_params=rating_f)
            body["properties"]["评分"] = tmp_dict

        # 评分人数
        if data_dict[MediaInfo.ASSESS.value]:
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.NUMBER.value,
                                                property_params=data_dict[MediaInfo.ASSESS.value])
            body["properties"]["评分人数"] = tmp_dict
        return body
    elif media_type == MediaType.MOVIE.value:

        # 导演 编剧 主演
        text_director = ' / '.join(data_dict[MediaInfo.DIRECTOR.value])
        text_screenwriter = ' / '.join(data_dict[MediaInfo.SCREENWRITER.value])
        text_starring = ' / '.join(data_dict[MediaInfo.STARRING.value])
        str_type = get_multi_select_body(data_dict[MediaInfo.MOVIE_TYPE.value])
        json_type = json.loads(str_type)
        str_c_or_r = get_multi_select_body(data_dict[MediaInfo.C_OR_R.value])
        json_c_or_r = json.loads(str_c_or_r)
        body = {
            "parent": {
                "type": "database_id",
                "database_id": f"{database_id}"
            },
            "properties": {
                "名字": {
                    "title": [{
                        "type": "text",
                        "text": {
                            "content": data_dict[MediaInfo.TITLE.value]
                        }
                    }]
                },
                "导演": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": text_director
                        }
                    }]
                },
                "编剧": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": text_screenwriter
                        }
                    }]
                },
                "主演": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": text_starring
                        }
                    }]
                },
                "类型": {
                    "multi_select": json_type
                },
                "国家地区": {
                    "multi_select": json_c_or_r
                },
                "IMDb": {
                    "url": f"https://www.imdb.com/title/{data_dict[MediaInfo.IMDB.value]}"
                },
                "标记状态": {
                    "select": {
                        "name": f"{status}"
                    }
                },
                "分类": {
                    "select": {
                        "name": f"{data_dict[MediaInfo.CATEGORIES.value]}"
                    }
                },
                "简介": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": data_dict[MediaInfo.RELATED.value]
                        }
                    }]
                },
                "封面": {
                    "files": [{
                        "type": "external",
                        "name": data_dict[MediaInfo.IMG.value][-15:],
                        "external": {
                            "url": data_dict[MediaInfo.IMG.value]
                        }
                    }]
                },
                "豆瓣链接": {
                    "url": f"{data_dict[MediaInfo.URL.value]}"
                },
                "短评": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": data_dict[MediaInfo.MY_COMMENT.value]
                        }
                    }]
                }
            }
        }

        # 评分
        if data_dict[MediaInfo.RATING_F.value]:
            rating_f = float(data_dict[MediaInfo.RATING_F.value])
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.NUMBER.value,
                                                property_params=rating_f)
            body["properties"]["评分"] = tmp_dict

        # 评分人数
        if data_dict[MediaInfo.ASSESS.value]:
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.NUMBER.value,
                                                property_params=data_dict[MediaInfo.ASSESS.value])
            body["properties"]["评分人数"] = tmp_dict

        # 标记日期
        if data_dict[MediaInfo.MY_DATE.value]:
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.DATE.value,
                                                property_params=data_dict[MediaInfo.MY_DATE.value])
            body["properties"]["标记时间"] = tmp_dict

        # 个人评分
        if data_dict[MediaInfo.MY_RATING.value]:
            tmp_dict = get_my_rate(data_dict)
            body["properties"]["个人评分"] = tmp_dict
        # 出版年份
        if data_dict[MediaInfo.RELEASE_DATE.value]:
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.SELECT.value,
                                                property_params=data_dict[MediaInfo.RELEASE_DATE.value][0:4])
            body["properties"]["时间"] = tmp_dict
        return body
    elif media_type == MediaType.BOOK.value:
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
                            "content": data_dict[
                                           MediaInfo.TITLE.value] + f"：{data_dict[MediaInfo.SUBHEAD.value]}" if data_dict.get(
                                MediaInfo.SUBHEAD.value) else data_dict[MediaInfo.TITLE.value]
                        }
                    }]
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
                "作者": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": data_dict[MediaInfo.AUTHOR.value]
                        }
                    }]
                },
                "标记状态": {
                    "select": {
                        "name": f"{status}"
                    }
                },
                "豆瓣链接": {
                    "url": f"{data_dict[MediaInfo.URL.value]}"
                },
                "短评": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": data_dict[MediaInfo.MY_COMMENT.value]
                        }
                    }]
                },
                "简介": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": data_dict[MediaInfo.RELATED.value]
                        }
                    }]
                }
            }
        }

        #  ISBN
        if data_dict[MediaInfo.ISBN.value]:
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.URL.value,
                                                property_params=data_dict[MediaInfo.ISBN.value])
            body["properties"]["ISBN"] = tmp_dict

        # 价格
        if data_dict[MediaInfo.PRICE.value]:
            tmp_float = float(data_dict[MediaInfo.PRICE.value])
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.NUMBER.value,
                                                property_params=tmp_float)
            body["properties"]["价格"] = tmp_dict

        # 评分
        if data_dict[MediaInfo.RATING_F.value]:
            rating_f = float(data_dict[MediaInfo.RATING_F.value])
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.NUMBER.value,
                                                property_params=rating_f)
            body["properties"]["评分"] = tmp_dict

        # 评分人数
        if data_dict[MediaInfo.ASSESS.value]:
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.NUMBER.value,
                                                property_params=data_dict[MediaInfo.ASSESS.value])
            body["properties"]["评分人数"] = tmp_dict

        # 页数
        page = data_dict[MediaInfo.PAGES.value]
        if page:
            pages_num = 1
            try:
                if page.endswith("页"):
                    page = page[:-1]
                pages_num = round(float(page))
            except Exception:
                pass
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.NUMBER.value,
                                                property_params=pages_num)
            body["properties"]["页数"] = tmp_dict

        # 出版社
        if data_dict[MediaInfo.PUBLISHER.value]:
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.SELECT.value,
                                                property_params=data_dict[MediaInfo.PUBLISHER.value])
            body["properties"]["出版社"] = tmp_dict

        # 标记日期
        if data_dict[MediaInfo.MY_DATE.value]:
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.DATE.value,
                                                property_params=data_dict[MediaInfo.MY_DATE.value])
            body["properties"]["标记时间"] = tmp_dict

        # 个人评分
        if data_dict[MediaInfo.MY_RATING.value]:
            tmp_dict = get_my_rate(data_dict)
            body["properties"]["个人评分"] = tmp_dict

        # 出版年份
        if data_dict[MediaInfo.PUB_DATE.value]:
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.SELECT.value,
                                                property_params=data_dict[MediaInfo.PUB_DATE.value][0:4])
            body["properties"]["出版年份"] = tmp_dict
        return body
    elif media_type == MediaType.GAME.value:
        str_game_type = get_multi_select_body(data_dict[MediaInfo.GAME_TYPE.value])
        json_game_type = json.loads(str_game_type)
        str_platform = get_multi_select_body(data_dict[MediaInfo.GAME_PLATFORM.value])
        json_platform = json.loads(str_platform)
        body = {
            "parent": {
                "type": "database_id",
                "database_id": f"{database_id}"
            },
            "properties": {
                "游戏名": {
                    "title": [{
                        "type": "text",
                        "text": {
                            "content": data_dict[MediaInfo.TITLE.value]
                        }
                    }]
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
                "标记状态": {
                    "select": {
                        "name": f"{game_status}"
                    }
                },
                "豆瓣链接": {
                    "url": f"{data_dict[MediaInfo.URL.value]}"
                },
                "短评": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": data_dict[MediaInfo.MY_COMMENT.value]
                        }
                    }]
                },
                "类型": {
                    "multi_select": json_game_type
                },
                "平台": {
                    "multi_select": json_platform
                }

            }
        }

        # 评分
        if data_dict[MediaInfo.RATING_F.value]:
            rating_f = float(data_dict[MediaInfo.RATING_F.value])
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.NUMBER.value,
                                                property_params=rating_f)
            body["properties"]["评分"] = tmp_dict

        # 评分人数
        if data_dict[MediaInfo.ASSESS.value]:
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.NUMBER.value,
                                                property_params=data_dict[MediaInfo.ASSESS.value])
            body["properties"]["评分人数"] = tmp_dict

        # 标记日期
        if data_dict[MediaInfo.MY_DATE.value]:
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.DATE.value,
                                                property_params=data_dict[MediaInfo.MY_DATE.value])
            body["properties"]["标记时间"] = tmp_dict

        # 个人评分
        if data_dict[MediaInfo.MY_RATING.value]:
            tmp_dict = get_my_rate(data_dict)
            body["properties"]["个人评分"] = tmp_dict

        # 发行日期
        if data_dict[MediaInfo.GAME_DATE.value]:
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.DATE.value,
                                                property_params=data_dict[MediaInfo.GAME_DATE.value])
            body["properties"]["发行日期"] = tmp_dict

        # 开发商
        if data_dict[MediaInfo.GAME_DEV.value]:
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.SELECT.value,
                                                property_params=data_dict[MediaInfo.GAME_DEV.value])
            body["properties"]["开发商"] = tmp_dict

        # 发行商
        if data_dict[MediaInfo.GAME_PUB.value]:
            tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.SELECT.value,
                                                property_params=data_dict[MediaInfo.GAME_PUB.value])
            body["properties"]["发行商"] = tmp_dict
        return body


def get_my_rate(data_dict):
    body_dict = {}
    value_num = data_dict[MediaInfo.MY_RATING.value]
    if value_num == "1":
        tmp_dict = {}
        tmp_dict.update(name="⭐")
        tmp_dict.update(color="yellow")
        body_dict.update(select=tmp_dict)
    elif value_num == "2":
        tmp_dict = {}
        tmp_dict.update(name="⭐⭐")
        tmp_dict.update(color="yellow")
        body_dict.update(select=tmp_dict)
    elif value_num == "3":
        tmp_dict = {}
        tmp_dict.update(name="⭐⭐⭐")
        tmp_dict.update(color="yellow")
        body_dict.update(select=tmp_dict)
    elif value_num == "4":
        tmp_dict = {}
        tmp_dict.update(name="⭐⭐⭐⭐")
        tmp_dict.update(color="yellow")
        body_dict.update(select=tmp_dict)
    elif value_num == "5":
        tmp_dict = {}
        tmp_dict.update(name="⭐⭐⭐⭐⭐")
        tmp_dict.update(color="yellow")
        body_dict.update(select=tmp_dict)
    return body_dict


def create_database(token, page_id, media_type):
    """
    创建新的数据库
    :param media_type: 媒体类型 book music tv movie
    :param token: notion->setting->integrations->develop your own integrations
    :param page_id: 浏览器打开notion，链接的尾部获取
    :return: databases_id，可以通过该id定位到数据库
    """
    # TODO 添加书 影 音 数据库
    create_db_data = {}
    if media_type == MediaType.BOOK.value:
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
                "封面": {"files": {}},
                "出版年份": {"select": {}},
                "价格": {"number": {}},
                "评分人数": {"number": {}},
                "页数": {"number": {}},
                "短评": {"rich_text": {}},
                "类型": {"multi_select": {}},
                "标记状态": {"select": {}},
                "标记时间": {"date": {}},
                "简介": {"rich_text": {}},
                "个人评分": {"select": {"options": [
                    {"name": "⭐", "color": "yellow"},
                    {"name": "⭐⭐", "color": "yellow"},
                    {"name": "⭐⭐⭐", "color": "yellow"},
                    {"name": "⭐⭐⭐⭐", "color": "yellow"},
                    {"name": "⭐⭐⭐⭐⭐", "color": "yellow"}]}},
            }}
    elif media_type == MediaType.MUSIC.value:
        create_db_data = {
            "parent": {"type": "page_id", "page_id": f"{page_id}"},
            "title": [{"type": "text", "text": {"content": "豆瓣音乐库"}}],
            "icon": {"type": "emoji", "emoji": "🎵"},
            "properties": {
                "音乐": {"title": {}},
                "表演者": {"rich_text": {}},
                "封面": {"files": {}},
                "评分": {"number": {}},
                "出版者": {"select": {}},
                "发行时间": {"select": {}},
                "ISRC": {"url": {}},
                "豆瓣链接": {"url": {}},
                "评分人数": {"number": {}},
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
    elif media_type == MediaType.MOVIE.value:
        """
        类型是获取豆瓣中的信息
            剧情 / 动作 / 科幻/ 犯罪
        分类是个人主观分的
            电视剧、电影、动画片（指的是电影）、动漫（剧集）、纪录片（电影和电视剧）
        """
        create_db_data = {
            "parent": {"type": "page_id", "page_id": f"{page_id}"},
            "title": [{"type": "text", "text": {"content": "豆瓣影视库"}}],
            "icon": {"type": "emoji", "emoji": "🎬"},
            "properties": {
                "名字": {"title": {}},
                "评分": {"number": {}},
                "豆瓣链接": {"url": {}},
                "导演": {"rich_text": {}},
                "编剧": {"rich_text": {}},
                "主演": {"rich_text": {}},
                "类型": {"multi_select": {}},
                "分类": {"select": {}},
                "国家地区": {"multi_select": {}},
                "IMDb": {"url": {}},
                "封面": {"files": {}},
                "时间": {"select": {}},
                "片长": {"number": {}},
                "评分人数": {"number": {}},
                "简介": {"rich_text": {}},
                "短评": {"rich_text": {}},
                "标记状态": {"select": {}},
                "标记时间": {"date": {}},
                "个人评分": {"select": {"options": [
                    {"name": "⭐", "color": "yellow"},
                    {"name": "⭐⭐", "color": "yellow"},
                    {"name": "⭐⭐⭐", "color": "yellow"},
                    {"name": "⭐⭐⭐⭐", "color": "yellow"},
                    {"name": "⭐⭐⭐⭐⭐", "color": "yellow"}]}},
            }}
    elif media_type == MediaType.GAME.value:
        create_db_data = {
            "parent": {"type": "page_id", "page_id": f"{page_id}"},
            "title": [{"type": "text", "text": {"content": "豆瓣游戏库"}}],
            "icon": {"type": "emoji", "emoji": "🎮"},
            "properties": {
                "游戏名": {"title": {}},
                "评分": {"number": {}},
                "豆瓣链接": {"url": {}},
                "开发商": {"select": {}},
                "发行商": {"select": {}},
                "类型": {"multi_select": {}},
                "平台": {"multi_select": {}},
                "发行日期": {"date": {}},
                "评分人数": {"number": {}},
                "短评": {"rich_text": {}},
                "标记状态": {"select": {}},
                "标记时间": {"date": {}},
                "封面": {"files": {}},
                "个人评分": {"select": {"options": [
                    {"name": "⭐", "color": "yellow"},
                    {"name": "⭐⭐", "color": "yellow"},
                    {"name": "⭐⭐⭐", "color": "yellow"},
                    {"name": "⭐⭐⭐⭐", "color": "yellow"},
                    {"name": "⭐⭐⭐⭐⭐", "color": "yellow"}]}},
            }}
    else:
        exit("暂不支持其他数据库的创建")

    try:
        if create_db_data:
            log_detail.info(f"【RNU】创建{media_type}数据库--初始化参数")
            db_data = base.NotionBaseInfo(token=token)
            params = json.dumps(create_db_data)
            # print(params)
            log_detail.debug(f"【RNU】创建{media_type}数据库--post请求")
            # res = RequestUtils.post(url=db_data.get_db_url(), params=params, headers=db_data.get_headers())
            db_res = RequestUtils()
            res = db_res.post(url=db_data.get_db_url(), params=params, headers=db_data.get_headers())
            if res.status_code == 200:
                log_detail.debug(res.text)
                database_id = eval(res.text.replace(":null", ":'null'").replace(":false", ":'false'"))["id"]
                return database_id
            else:
                exit("创建数据库失败，请检查是否页面有授权给【集权】，再重新使用本程序")
        else:
            log_detail.warn(f"【RUN】跳过创建{media_type}数据库")
    except Exception as err:
        exit(f"网络请求错误:{err}")


def get_flag_update_database(data_dict, database_id, token, media_status, media_type):
    """
    写入数据库

    :param media_type: 媒体类型
    :param data_dict: 待写入数据字典
    :param database_id: 数据库id
    :param token:【必须】
    :param media_status: 标记状态
    :return: TODO 返回一个成功后的页面ID
    """
    try:
        body = get_body(data_dict=data_dict,
                        database_id=database_id,
                        media_status=media_status,
                        media_type=media_type)
        body = json.dumps(body)
        page_data = base.NotionBaseInfo(token)
        req = RequestUtils()
        res = req.post(url=page_data.get_page_url(),
                       headers=page_data.get_headers(),
                       params=body)
        if res.status_code == 200:
            # log_detail.info(f'【RUN】- 导入《{data_dict[MediaInfo.TITLE.value]}》成功。媒体链接：{data_dict["url"]}')
            return "succeed"
        else:
            log_detail.warn(f'【RUN】导入失败：{res.content}！')
            return "failed"
    except Exception as err:
        log_detail.error(f'【RUN】导入异常：{err}！')
        return "exception"


def get_flag_update_old_database(data_dict, page_id, token, media_status, media_type):
    """
    更新数据库

    :param media_type: 媒体类型
    :param data_dict: 待写入数据字典
    :param page_id: 页面ID
    :param token:【必须】
    :param media_status: 标记状态
    :return: TODO 返回一个成功后的页面ID
    """
    try:
        body = get_new_update_body(data_dict=data_dict,
                                   media_status=media_status,
                                   media_type=media_type)
        body = json.dumps(body)
        page_data = base.NotionBaseInfo(token)
        req = RequestUtils()
        res = req.patch(url=page_data.get_page_url() + f"/{page_id}",
                        headers=page_data.get_headers(),
                        params=body)
        if res.status_code == 200:
            # log_detail.info(f'【RUN】- 导入《{data_dict[MediaInfo.TITLE.value]}》成功。媒体链接：{data_dict["url"]}')
            return "succeed"
        else:
            log_detail.warn(f'【RUN】导入失败：{res.content}！')
            return "failed"
    except Exception as err:
        log_detail.error(f'【RUN】导入异常：{err}！')
        return "exception"


def get_new_update_body(data_dict, media_status, media_type):
    music_status, status, game_status = get_media_status(media_status)

    log_detail.info(f"【RUN】- {media_type}数据信息整理为json格式")
    if media_type == MediaType.MUSIC.value:
        body = {
            "properties": {
                "标记状态": {
                    "select": {
                        "name": f"{music_status}"
                    }
                }
            }
        }
        return body
    elif media_type == MediaType.MOVIE.value:
        return get_common_body(data_dict, status)
    elif media_type == MediaType.BOOK.value:
        return get_common_body(data_dict, status)
    elif media_type == MediaType.GAME.value:
        return get_common_body(data_dict, game_status)


def get_media_status(media_status):
    if media_status == MediaStatus.WISH.value:
        status = "想看"
        music_status = "想听"
        game_status = "想玩"
    elif media_status == MediaStatus.DO.value:
        status = "在看"
        music_status = "在听"
        game_status = "在玩"
    elif media_status == MediaStatus.COLLECT.value:
        status = "看过"
        music_status = "听过"
        game_status = "玩过"
    else:
        status = ""
        music_status = ""
        game_status = ""
    return music_status, status, game_status


def get_common_body(data_dict, status):
    body = {
        "properties": {
            "标记状态": {
                "select": {
                    "name": f"{status}"
                }
            },
            "短评": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": data_dict[MediaInfo.MY_COMMENT.value]
                    }
                }]
            }
        }
    }
    # 个人评分
    if data_dict[MediaInfo.MY_RATING.value]:
        tmp_dict = get_my_rate(data_dict)
        body["properties"]["个人评分"] = tmp_dict
    # 标记日期
    if data_dict[MediaInfo.MY_DATE.value]:
        tmp_dict = get_non_null_params_body(property_type=DatabaseProperty.DATE.value,
                                            property_params=data_dict[MediaInfo.MY_DATE.value])
        body["properties"]["标记时间"] = tmp_dict
    return body
