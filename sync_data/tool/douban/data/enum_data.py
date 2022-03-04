# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/2/26 01:05
# @Function: 枚举所用到的数据


from enum import Enum


class MediaType(Enum):
    """
    豆瓣三大类：影音书
    """
    BOOK = "book"
    MOVIE = "movie"
    MUSIC = "music"


class MediaStatus(Enum):
    """
    个人影音书的标记状态
    """
    DO = "do"
    WISH = "wish"
    COLLECT = "collect"


class MediaInfo(Enum):
    """
    媒体信息
    """
    # 通用 默认为字符串str, 后面加_F则为float型
    # 评分 个人评分 简介 短评
    TITLE = "title"                     # 媒体名称
    STATUS = "status"                   # 标记
    STATUS_DATE = "status_date"         # 标记日期
    IMG = "img"                         # 封面、海报
    URL = "url"                         # 链接
    TAG_LIST = "tag_list"               # 标签
    RATING_F = "rating"                 # 评分
    ASSESS = 'assess'                   # 评价数

    # 书籍
    AUTHOR = "author"                   # 作者
    PUBLISHER = "publisher"             # 出版社
    PUB_DATE = "pub_date"               # 出版日期
    PRICE = "price"                     # 价格
    ISBN = 'isbn'                       # ISBN
    SUBHEAD = 'book_subhead'            # 副标题
    PAGES = 'pages'                     # 页数


class MediaXpathParam(Enum):
    """
    提取html的参数
    """
    # 书籍详情页获取信息
    B_NAME = '//span[@property="v:itemreviewed"]/text()'
    B_RATING_NUM = '//strong[@class="ll rating_num "][@property="v:average"]/text()'
    B_AUTHOR = '//div[@id="info"][@class]/span/a[@class][@href]/text()'
    B_PUB = '//div[@class="subject clearfix"]/div[@id="info"]/text()'
    B_SHORT = '//span[@class="short"]/div[@class="intro"]//following-sibling::*'

    # 个人状态页面[wish/do/collect]获取信息
    LIST_BOOK_URL = '//div[@class="pic"]/a[@class="nbg"]/@href'
    LIST_BOOK_NAME = '//div[@class="info"]/h2/a/@title'
    LIST_BOOK_DATE_STATUS = '//div[@class="short-note"]/div/span[@class="date"]/text()'
    LIST_BOOK_PIC = '//li[@class="subject-item"]/div[@class="pic"]/a/img/@sync_data'
    LIST_BOOK_PUB = '//div[@class="info"]/div[@class="pub"]/text()'

