# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/3/1 21:05
# @Function: 程序入口

import argparse
import os
import sys

from sync_data.app.sync import start_sync, init_database
from sync_data.utils import log_detail
from sync_data.utils.config import Config
from sync_data.version import version as ver


def get_version():
    return ver


# 命令行参数
arg_parser = argparse.ArgumentParser(description="导入数据至notion数据库")
arg_parser.add_argument('-m',
                        '--media',
                        help='输入模式，book/movie/tv/music')
arg_parser.add_argument('-s',
                        '--status',
                        help='输入媒体状态，wish/do/collect/all')

arg_parser.add_argument('-f',
                        '--func',
                        help='功能参数，init --初始化数据库')

arg_parser.add_argument('-v',
                        '--version',
                        action='version',
                        version=get_version(),
                        help='版本信息')


if __name__ == '__main__':

    args = arg_parser.parse_args()
    media = args.media
    status = args.status
    func = args.func

    if media in ['book', 'music', 'tv', 'movie'] and status in ['do', 'wish', 'collect', 'all']:
        if func is not None:
            log_detail.warn("【Tip】参数过多，不做处理，退出程序")
            exit()
        else:
            if media in ['tv', 'movie']:
                log_detail.warn("【Tip】暂不支持该功能，请调整命令，再试一次！")
                exit()
            if status == 'all':
                for i in ['do', 'wish', 'collect']:
                    log_detail.info(f"【RUN】开始获取{media}的{i}状态信息")
                    start_sync(media_type=media, media_status=i)
            else:
                log_detail.info("----开始拉取数据----")
                start_sync(media_type=media, media_status=status)
    elif media is not None or status is not None:
        log_detail.warn(f'【Tip】您输入的-m参数为< {media} >,请输入< python run.py -h >查看正确指令')
        log_detail.warn(f'【Tip】您输入的-s参数为< {status} >,请输入< python run.py -h >查看正确指令')
    elif func == 'init':
        print("初始化数据库")
        init_database()
        log_detail.info("【Tip】请在浏览器查看您的notion页面，并将新创建的数据库id填入到config.yaml。")
    elif func is not None:
        log_detail.info(f'【Tip】您输入的-f参数为< {func} >，请输入< python run.py -h >查看正确指令')
    else:
        log_detail.info(f'【Tip】请输入< python run.py -h >查看正确指令')

    log_detail.info("【RUN】程序结束！")

