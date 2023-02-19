# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/3/1 21:05
# @Function: 处理配置文件

import logging
import os
import threading

import yaml

from sync_data.utils import log_detail

# 抄作业 https://github.com/jxxghp/nas-tools/blob/master/config.py

# 日志级别
LOG_LEVEL = logging.INFO
lock = threading.Lock()


class Config(object):
    __config = {}
    __instance = None
    __config_path = None

    def __init__(self):
        self.__config_path = os.path.abspath(os.path.join(os.getcwd(), "./doc/config.yaml"))
        # print("获取配置文件路径：%s" % self.__config_path)
        self.load_config()

    @staticmethod
    def __get_config_path(self):
        return os.path.abspath(os.path.join(os.getcwd(), "./doc/config.yaml"))

    @staticmethod
    def get_instance():
        if Config.__instance:
            return Config.__instance
        try:
            lock.acquire()
            if not Config.__config:
                Config.__instance = Config()
        finally:
            lock.release()
        return Config.__instance

    def load_config(self):
        try:
            if not os.path.exists(self.__config_path):
                print("【RUN】配置文件不存在，请复制/doc/config.yaml.simple 到本目录为config.yaml，再重新启动")
                quit()
            with open(self.__config_path, 'r', encoding='utf-8') as file:
                self.__config = yaml.safe_load(file)
        except yaml.YAMLError as err:
            print("读取配置文件错误：%s" % str(err))
            return False

    def get_config(self):
        return self.__config

    def save_config(self, new_config):
        self.__config = new_config
        with open(self.__config_path, mode='w', encoding='utf-8') as file:
            return yaml.dump(new_config, file, allow_unicode=True)

    def get_config_path(self):
        return self.__config_path


# 得到配置信息
def get_config():
    return Config.get_instance().get_config()


# 得到配置路径
def get_config_path():
    return Config.get_instance().get_config_path()


# 装载配置
def load_config():
    return Config.get_instance().load_config()


# 保存配置
def save_config(new_config):
    return Config.get_instance().save_cnfig(new_config)


# 自动配置notion数据库id
def auto_config_database(media_type, database_id):
    """
    自动配置数据库id

    :param media_type: 'book', 'music', 'movie'
    :param database_id: 32位id
    :return:
    """

    try:
        if media_type in ['book', 'music', 'movie', 'game'] and len(database_id) == 32:
            auto_conf = get_auto_config()
            auto_conf_path = get_auto_conf_path()
            auto_conf[f'{media_type}_database_id'] = database_id
            with open(auto_conf_path, mode='w', encoding='utf-8') as file:
                yaml.dump(auto_conf, file, allow_unicode=True)
            return "succeed"
        else:
            log_detail.warn(
                f"【RUN】传入参数media_type:<{media_type}>,db_id:<{database_id}>,数据库id长度为:<{len(database_id)}>存在错误")
            return "failed"
    except Exception as err:
        log_detail.error(f"【RUN】{err}")
        return "failed"


def save_auto_config(new_config):
    try:
        auto_conf_path = get_auto_conf_path()
        with open(auto_conf_path, mode='w', encoding='utf-8') as file:
            yaml.dump(new_config, file, allow_unicode=True)
        return "succeed"
    except Exception as err:
        log_detail.error(f"【RUN】自动保存配置失败：{err}")
        return "failed"


def get_auto_conf_path():
    base_path = Config().get_config_path()
    auto_conf_path = base_path.replace('config', 'auto')
    # log_detail.info(f"【RUN】自动配置路径为：\t{auto_conf_path}")
    return auto_conf_path


def get_auto_config():
    auto_conf_path = get_auto_conf_path()

    if not os.path.exists(auto_conf_path):
        log_detail.info("【RUN】自动配置文件不存在，将会自动创建auto.yaml文件")
        auto_config = {"book_database_id": "",
                       "music_database_id": "",
                       "movie_database_id": "",
                       "game_database_id": ""
                       }
        with open(auto_conf_path, mode='w', encoding='utf-8') as file:
            yaml.dump(auto_config, file, allow_unicode=True)
        return auto_config
    else:
        log_detail.info("【RUN】读取程序自动配置的文件[auto.yaml]")
        with open(auto_conf_path, 'r', encoding='utf-8') as file:
            auto_conf = yaml.safe_load(file)
        return auto_conf


# 检查配置信息


# 测试
if __name__ == '__main__':
    config_dict = get_config()
    print(config_dict)
