============
版本日志
============

说明
========

:alpha: 先行版
:beta: 测试版
:v0.x.x: 稳定版
:release: 最终版（某一功能稳定后发布）


[Unreleased]
============
`[v0.1.4-alpha] <https://github.com/Qliangw/notion_sync_data/compare/v0.1.3-alpha...v0.1.4-alpha>`_ - 2023-03-10
========================
- 新增Github Actions自动同步 `[pr#26] <https://github.com/Qliangw/notion_sync_data/pull/26>`_
- 修复电影导入失败的问题

`[v0.1.3-alpha] <https://github.com/Qliangw/notion_sync_data/compare/v0.1.2-release...v0.1.3-alpha>`_ - 2023-03-10
========================
- fix: 修复因标记日期导入失败的问题 `[issues#22] <https://github.com/Qliangw/notion_sync_data/issues/22>`_

`[v0.1.2-release] <https://github.com/Qliangw/notion_sync_data/compare/v0.1.2-beta...v0.1.2-release>`_ - 2023-03-06
========================
- fix: 修复初始化失败的问题

`[v0.1.2-beta] <https://github.com/Qliangw/notion_sync_data/compare/v0.1.2-alpha...v0.1.2-beta>`_ - 2023-02-20
========================
- fix: 修复导入某些项目失败的问题 `[pr#20] <https://github.com/Qliangw/notion_sync_data/pull/20>`_
- feat: 新增游戏库的支持
- style: 变成配置文件，合并成为统一的配置文件（为GUI做准备）

.. tip::
    - 更新后请先运行 python run.py -f config

`[v0.1.2-beta] <https://github.com/Qliangw/notion_sync_data/compare/v0.1.2-alpha...v0.1.2-beta>`_ - 2023-02-20
========================

`[v0.1.2-alpha] <https://github.com/Qliangw/notion_sync_data/compare/v0.1.1...v0.1.2-alpha>`_ - 2022-08-23
========================
- fix: 修初始化数据库失败的问题 `[issues#18] <https://github.com/Qliangw/notion_sync_data/issues/18>`_


`[v0.1.1] <https://github.com/Qliangw/notion_sync_data/compare/v0.1.1-beta...v0.1.1>`_ - 2022-03-16
========================
- fix: 修复书籍信息（出版社、评分、评分人数、页数等）不全无法正常导入的问题

- fix(sync): 修复notion已存在时输入日志的问题
- fix(parser): 修复访问多页时临界值问题
- feat: notion数据库参数分离
- style: 冗余代码函数化
- refactor: 调整日志输出格式

.. tip::

    - 大概没有太多严重问题了

    - TODO: 有时间学学界面化搞GUI，不想再用命令导入了！

`[v0.1.1-beta] <https://github.com/Qliangw/notion_sync_data/compare/v0.1.1-alpha...v0.1.1-beta>`_ - 2022-03-14
========================

- fix(douban): 修复 `[issues#7] <https://github.com/Qliangw/notion_sync_data/issues/7>`_ 豆瓣电影信息不全（导演、编剧、主演、类型、国家或地区、语言）时异常的问题


`[v0.1.1-alpha] <https://github.com/Qliangw/notion_sync_data/compare/v0.1.0-beta...v0.1.1-alpha>`_ - 2022-03-14
========================

- style: 调整日志输出内容
- feat: 增加监控日期的功能
- feat: 用户信息脱敏处理

.. tip::
    有关监控日期的使用请看： `[config.yaml] <https://github.com/Qliangw/notion_sync_data/blob/main/doc/config.yaml.simple>`_ 中 ``douban -> day`` 参数的说明

`[v0.1.0-beta] <https://github.com/Qliangw/notion_sync_data/compare/v0.1.0-alpha...v0.1.0-beta>`_ - 2022-03-12
========================
- fix(douan): 修复一些解析问题
- fix(douban): 修复访问豆瓣网页失败时无法正常执行的问题
- feat(sync): 添加成功、失败、跳过的计数

`[v0.1.0-alpha] <https://github.com/Qliangw/notion_sync_data/compare/v0.0.7-beta...v0.1.0-alpha>`_ - 2022-03-11
========================

- feat: 影视信息的导入
- fix: 因网络问题导致的程序异常

`[v0.0.7-beta] <https://github.com/Qliangw/notion_sync_data/compare/v0.0.7-alpha...v0.0.7-beta>`_ - 2022-03-10
========================

- feat: 初始化数据库后，自动保存数据库id
- fix(run): 解决添加版本信息后参数冲突的问题

`[v0.0.7-alpha] <https://github.com/Qliangw/notion_sync_data/compare/v0.0.6-beta...v0.0.7-alpha>`_ - 2022-03-10
========================

- fix(run.py): `issues#4 <https://github.com/Qliangw/notion_sync_data/issues/4>`_ ，使用-s all参数报错的问题
- feat: 通过-v 或者--version可查询版本号
- docs: update

[v0.0.6-beta] - 2022-03-08
========================
- 无

[0.0.6-alpha] - 2022-03-08
========================
- 修复出版社有[,]不能插入的Bug
- 修复无评分、无评分人数不能插入的Bug

2022-03-07
========================

- 增加音乐数据的获取
- 配置内容的更新【重要】
- 修复书籍价格为空时程序异常的Bug

2022-03-06
========================

- fix：增加过滤功能，数据不再重复添加


2022-03-04
========================

- 支持豆瓣书籍的导入