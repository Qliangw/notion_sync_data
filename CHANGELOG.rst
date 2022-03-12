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

- fix(run.py): `issues-4 <https://github.com/Qliangw/notion_sync_data/issues/4>`_ ，使用-s all参数报错的问题
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