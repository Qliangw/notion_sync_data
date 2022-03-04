# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/3/1 21:05
# @Function: 使用bs4查找html相关数据
import re

from bs4 import BeautifulSoup
from sync_data.tool.douban.data.enum_data import MediaType, MediaInfo
from sync_data.utils import log_detail

# 解析参考 https://zhuanlan.zhihu.com/p/54195299


class ParserHtmlText:
    """
    使用BeautifulSoup解析html
    """
    def __init__(self, html_text):
        self.html = html_text
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def get_url_list(self):
        """
        解析个人wish/do/collect内容的每个url

        :return: url数组
        """
        url_list = []
        try:
            info = self.soup.select('.nbg')
            for url in info:
                url_list.append(url.get('href'))
            return url_list
        except Exception as err:
            log_detail.info(f"解析失败：{err}")
            return None

    def get_parser_dict(self, media_type):
        """
        解析网页，抓取数据

        :param media_type: 媒体类型，使用enum_data的枚举类
        :return: 数据字典，提取key在enum_data的MediaInfo中
        """
        try:
            self.__parser(media_type=media_type)
            return self.dict
        except Exception as err:
            log_detail.info("解析失败")
            return None

    def __parser(self, media_type):
        # parser_dict = {}
        # soup = BeautifulSoup(self.html, 'lxml')
        # self.soup = BeautifulSoup(self.html, 'html.parser')
        if media_type == MediaType.BOOK.value:
            self.dict = self.__get_book_dict()
        elif media_type == MediaType.MOVIE.value:
            pass
        elif media_type == MediaType.MUSIC.value:
            pass
        else:
            pass

    def __get_book_dict(self):
        log_detail.info("【RUN】解析书籍信息")
        # 标签名不加任何修饰，类名前加点，id名前加#
        info = self.soup.select('#info')
        infos = list(info[0].strings)
        infos = [i.strip() for i in infos if i.strip() != '']
        book_dict = {}

        # 书名
        book_title = self.soup.select('#wrapper > h1 > span')[0].contents[0]  # 书名

        # 作者
        if '作者:' in infos:
            book_author = infos[infos.index('作者:') + 1]
        elif self.soup.select('#info > span > a'):
            book_author = self.soup.select('#info > span > a')[0].contents[0]
        else:
            book_author = ""
        book_author = ''.join(map(str.strip, book_author.split('\n')))

        # 出版社 副标题 出版年 页数 定价 ISBN
        book_publisher = infos[infos.index('出版社:') + 1] if '出版社:' in infos else ""
        book_subhead = infos[infos.index('副标题:') + 1] if '副标题:' in infos else ""
        book_pub_date = infos[infos.index('出版年:') + 1] if '出版年:' in infos else ""
        book_pages = infos[infos.index('页数:') + 1] if '页数:' in infos else ""
        book_price = infos[infos.index('定价:') + 1] if '定价:' in infos else ""
        # https://isbnsearch.org/isbn/{ISBN}
        book_isbn = infos[infos.index('ISBN:') + 1] if 'ISBN:' in infos else ""

        # 评分 评价数 图片网址
        rating = self.soup.select("#interest_sectl > div > div.rating_self.clearfix > strong")
        book_rating = rating[0].contents[0] if rating else ""
        book_assesses = self.soup.select(
            "#interest_sectl > div > div.rating_self.clearfix > div > div.rating_sum > span > a > span")
        book_assess = book_assesses[0].contents[0] if book_assesses else ""
        book_img = self.soup.select("#mainpic > a > img")[0].attrs['src']

        book_price_list = [float(s) for s in re.findall(r'-?\d+\.?\d*', book_price)]
        book_price = book_price_list[0]

        book_dict[MediaInfo.TITLE.value] = book_title
        book_dict[MediaInfo.AUTHOR.value] = book_author
        book_dict[MediaInfo.PUBLISHER.value] = book_publisher
        book_dict[MediaInfo.SUBHEAD.value] = book_subhead
        book_dict[MediaInfo.PUB_DATE.value] = book_pub_date
        book_dict[MediaInfo.PAGES.value] = book_pages
        book_dict[MediaInfo.PRICE.value] = book_price
        book_dict[MediaInfo.ISBN.value] = book_isbn
        book_dict[MediaInfo.RATING_F.value] = book_rating
        book_dict[MediaInfo.ASSESS.value] = book_assess
        book_dict[MediaInfo.IMG.value] = book_img
        return book_dict

    def __tv(self):
        pass

    def __movie(self):
        pass

    def __music(self):
        pass



