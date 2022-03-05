# notion_sync_data
将网络数据中的个人标记媒体同步到notion笔记，方便快速查阅。

- 目前仅支持获取豆瓣书籍的信息

> 该库是学习python做的自用小工具，代码参考于网络。（首个用python编写的工具，写的比较烂）



**目录结构**

```
run.py # 主程序
|
sync_data/
├── app/
│   └── sync.py
├── data/
│   └── user_config.py
├── test/
│   └── test.py
├── tool/
│   ├── douban/			# 豆瓣获取信息工具
│   │   ├── base.py
│   │   ├── data/
│   │   └── soup/
│   └── notion/			# notion接口
│       ├── base.py
│       ├── databases.py
│       └── query.py
└── utils/
    ├── config.py
    ├── http_utils.py
    └── log_detail.py
```




## 功能

- [x] 获取豆瓣书籍
- [ ] 获取豆瓣电影
- [ ] 获取豆瓣剧集
- [ ] 获取豆瓣音乐
- [x] 创建notion数据库
- [x] 插入notion库

**TODO**

- [ ] 同步豆瓣内容
- [ ] 添加GUI
- [ ] 添加提取数据内容的获取



## 页面展示



![](https://raw.githubusercontent.com/Qliangw/notion_sync_data/main/img/gallery.png)



## [使用方法](https://github.com/Qliangw/notion_sync_data/wiki/Wiki#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95)





## 鸣谢



- 感谢 [jarrett-au](https://github.com/jarrett-au/douban2noition ) 

- 感谢 [Geetheshe](https://github.com/Geetheshe/DoubanMovieListBackUpToNotion ) 
- 感谢 [jxxghp](https://github.com/jxxghp/nas-tools) 

- 感谢靓仔
