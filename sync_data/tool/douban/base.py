# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/2/26 22:31
# @Function: 处理豆瓣的http请求

import requests.utils

from sync_data.utils.http_utils import RequestUtils
from sync_data.utils import log_detail


class DouBanBase:
    __headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}

    def __init__(self, user_agent=None, user_cookies=None):
        """
        初始化

        :param user_agent: 浏览器的user_agent，为空则填写默认【建议配置】
        :param user_cookies: 留空即可【用户cookie, 预留】
        """
        # user_agent为空，设为默认
        log_detail.info("DouBanBase初始化")
        if user_agent is None:
            log_detail.info("配置默认user-agent的值")
            self.headers = self.__headers
        else:
            log_detail.info("配置用户自定义user-agent的值")
            self.headers = {"User-Agent": f"{user_agent}"}

        # cookies为空，先访问一次首页
        if user_cookies is None:
            log_detail.info("访问豆瓣主页，配置默认cookie")
            try:
                self.req = RequestUtils(request_interval_mode=True)
                res = self.req.get_res("https://www.douban.com/", headers=self.headers)
                cookies = res.cookies
                cookie = requests.utils.dict_from_cookiejar(cookies)
                self.cookie = cookie
            except Exception as err:
                log_detail.info(f"获取cookie失败:{format(err)}")

        else:
            log_detail.info("配置用户自定义cookie")
            self.cookies = user_cookies

    def __set_cookies(self, res):
        if res.cookies.values() is None:
            log_detail.info(f"配置默认cookie：{res.cookies}")
            self.cookies = res.cookies.values()

    def __get_cookies(self):
        return self.cookie

    def __get_headers(self):
        return self.headers

    def get_html_text(self, url=None, user_id=None, media_type="book", media_status="wish", start_number=1):
        """
        获取链接的html文档

        :param url: 1. 如果为空，则默认配置一个链接，该链接为豆瓣用户的【想看（wish）】页面 | 2. url必须为某个书、影、音的详情页
        :param user_id: 用户id(如果url选择第二种则为空）
        :param media_type: 媒体类别（book/movie/music），可以通过../tool/douban/data/enum_data中的类获取。
        :param media_status: 状态（wish/do/collect），同上
        :param start_number: url为空时，该参数必填
        :return: html的text格式
        """

        # TODO 增加参数的判断，以及一些异常的处理
        if url is None:
            url = f"https://{media_type}.douban.com/people/{user_id}/{media_status}?start={start_number}&sort=time&rating=all&filter=all&mode=grid"

        headers = self.__get_headers()
        log_detail.info(f"获取headers：{headers}")
        cookies = self.__get_cookies()
        log_detail.info(f"获取cookies{cookies}")
        try:
            log_detail.info("请求url，获取返回值")
            res = self.req.get_res(url=url, headers=headers, cookies=cookies)
            res_text = res.text
            if res_text.find('有异常请求从你的 IP 发出') != -1:
                log_detail.info("被豆瓣识别到抓取行为了，请更换 IP 后才能使用")
                return None
            # return etree.HTML(res_text)
            return res_text
        except Exception as err:
            log_detail.info(f"获取{url}页面失败:{format(err)}")
            return None
