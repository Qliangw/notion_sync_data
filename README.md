# notion_sync_data
将网络数据同步到notion笔记，方便快速查阅。

[![GitHub stars](https://img.shields.io/github/stars/Qliangw/notion_sync_data?style=plastic)](https://github.com/Qliangw/notion_sync_data/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/Qliangw/notion_sync_data?style=plastic)](https://github.com/Qliangw/notion_sync_data/issues)

![Visitors](https://api.visitorbadge.io/api/combined?path=https%3A%2F%2Fgithub.com%2FQliangw%2Fnotion_sync_data&label=visitors&labelColor=%235d5d5d&countColor=%23d9e3f0&style=plastic)

- 目前已支持获取豆瓣【影、音、书】的信息的获取
- 测试平台：Windows、Linux[Ubuntu20.4/Debain10]
- 开发环境：Python 3.10.2（建议使用使用版本Python3.8+）

> 该库是学习python做的自用小工具，代码参考于网络。（首个用python编写的工具，写的比较烂）

**PR请申请合并至dev分支！！！**


**最新版本：**[v0.1.4-alpha](https://github.com/Qliangw/notion_sync_data/releases/tag/v0.1.4-alpha)


## 功能

- [x] 豆瓣【影、音、书】的信息
- [x] 创建notion数据库
- [x] 插入notion库
- [x] 已添加的不再重复添加（根据豆瓣链接判断）
- [x] Github Actions自动同步

**TODO**

### 鸽了那么久，更新了一下，只是修了notion调整的接口带来的Bug 

- [ ] 添加GUI（学习中
- [ ] notion根据豆瓣信息变化进行更新（标记状态、评分、评分人数）
- [ ] 主要针对书籍标记信息添加一列【阅读时间】
- [ ] [营养成分表](https://www.tianapi.com/apiview/121)

## [更新日志](https://github.com/Qliangw/notion_sync_data/blob/main/CHANGELOG.rst)

## [使用方法](https://qliangw.notion.site/)

## 页面展示

[豆瓣书单](https://qliangw.notion.site/25dbf612997f43f4a2a7f2156a11d3ae?v=05ce09bfaaaa46058215b13ad4b60b0d)

[豆瓣影视](https://qliangw.notion.site/fe986bd915ac49a2a587db9da3ffb9db?v=d8acb239433b4c9da9c7ec6107c882c2)


## 鸣谢

- 感谢 [jarrett-au](https://github.com/jarrett-au/douban2noition)
- 感谢 [Geetheshe](https://github.com/Geetheshe/DoubanMovieListBackUpToNotion) 
- 感谢 [jxxghp](https://github.com/jxxghp/nas-tools)
- 感谢靓仔
