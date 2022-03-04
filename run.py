# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/3/1 21:05
# @Function: 程序入口

import argparse
import os
import sys

from sync_data.app.sync import start_sync
from sync_data.utils import log_detail
from sync_data.utils.config import Config


# 命令行参数
arg_parser = argparse.ArgumentParser(description="导入数据至notion数据库")
arg_parser.add_argument('-m',
                        '--media',
                        default='book',
                        help='输入模式，book/movie/tv/music')
arg_parser.add_argument('-s',
                        '--status',
                        default='wish',
                        help='输入媒体状态：wish/do/collect')


if __name__ == '__main__':
    args = arg_parser.parse_args()
    media = args.media
    status = args.status
    print("您要导入的媒体为：", media)
    print("媒体标记为：", status)

    start_sync(media_type=media, media_status=status)
