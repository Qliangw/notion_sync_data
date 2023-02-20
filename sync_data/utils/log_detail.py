# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/3/1 21:05
# @Function: 格式化日志

import logging
import os
import threading
from logging.handlers import TimedRotatingFileHandler
from sync_data.utils.config import LOG_LEVEL, Config

lock = threading.Lock()


class Logger:
    __instance = None

    def __init__(self):
        self.logger = logging.Logger(__name__)
        self.logger.setLevel(level=LOG_LEVEL)
        user_config = Config().get_config()
        # self.logger.setLevel(logging.INFO)
        # log_type = user_config['app'].get('log_type', 'CONSOLE')

        if user_config['app']:
            log_type = user_config['app'].get('log_type', 'CONSOLE')
        else:
            log_type = "CONSOLE"

        if log_type == "FILE":
            # 记录日志到文件
            log_path = user_config['app'].get('log_path')
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            log_file_handler = TimedRotatingFileHandler(filename=log_path + "/" + __name__ + ".txt", when="D",
                                                        interval=1,
                                                        backupCount=2)
            formatter = logging.Formatter(
                '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s')
            log_file_handler.setFormatter(formatter)
            self.logger.addHandler(log_file_handler)
        elif log_type == "SERVER":
            log_server = user_config['app'].get('log_server')
            log_ip = log_server.split(':')[0]
            log_port = int(log_server.split(':')[1])
            log_server_handler = logging.handlers.SysLogHandler((log_ip, log_port),
                                                                logging.handlers.SysLogHandler.LOG_USER)
            formatter = logging.Formatter('%(filename)s: %(message)s')
            log_server_handler.setFormatter(formatter)
            self.logger.addHandler(log_server_handler)
        else:
            # 记录日志到终端
            log_console_handler = logging.StreamHandler()
            self.logger.addHandler(log_console_handler)

    @staticmethod
    def get_instance():
        if Logger.__instance:
            return Logger.__instance
        try:
            lock.acquire()
            if not Logger.__instance:
                Logger.__instance = Logger()
        finally:
            lock.release()
        return Logger.__instance


def debug(text):
    return Logger.get_instance().logger.debug(text)


def info(text):
    return Logger.get_instance().logger.info(text)


def error(text):
    return Logger.get_instance().logger.error(text)


def warn(text):
    return Logger.get_instance().logger.warning(text)
