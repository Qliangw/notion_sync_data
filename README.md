# notion_sync_data
将网络数据中的个人标记媒体同步到notion笔记，方便快速查阅。

- 目前仅只是豆瓣书籍的信息


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

## 使用

1. 下载该仓库 `git clone https://github.com/Qliangw/notion_sync_data.git`

2. 安装依赖环境 `pip install -r requirements.txt`

3. 复制`doc`文件下的`config.yaml.simple` 文件重命名为`config.yaml`

4. 根据`config.yaml`说明进行填写

   1. 豆瓣user_id的获取（cookie暂时没有用）

      登录豆瓣，点击个人主页，`douban.com/people/xxxx` 这个xxxx就是你的user_id

   2. user-agent建议填写

      打开豆瓣，按f12 再按f5，根据图片中内容查找

      <img src="https://raw.githubusercontent.com/Qliangw/notion_sync_data/main/img/user-agent.png" style="zoom: 50%;" />

      

   3. notion的token获取

      1.  打开notion的设置页面
      2.  按照图片去获取

      <img src="https://raw.githubusercontent.com/Qliangw/notion_sync_data/main/img/notion_token.png" style="zoom:50%;" />

      <img src="https://raw.githubusercontent.com/Qliangw/notion_sync_data/main/img/get_token.png" style="zoom:50%;" />

   4. notion的page_id获取【你要新建数据库的页面】

      <img src="https://raw.githubusercontent.com/Qliangw/notion_sync_data/main/img/page_id.png" style="zoom:50%;" />

   5. notion的database_id获取

5. `python run.py -h`查看帮助文档

   <img src="https://raw.githubusercontent.com/Qliangw/notion_sync_data/main/img/help.png" style="zoom: 80%;" />

6. `python run.py -f init` 初始化notion数据库

   <img src="https://raw.githubusercontent.com/Qliangw/notion_sync_data/main/img/init.png" style="zoom: 67%;" />

   ​	网页查看数据库

   <img src="https://raw.githubusercontent.com/Qliangw/notion_sync_data/main/img/notion_db.png" style="zoom: 50%;" />

7. 打开刚刚创建的数据库，复制数据库id到`config.yaml`对应位置

8. `python run.py -m book -s wish`
   1. 目前仅支持图书的 想看 、在看、 看过的导入

------

## 鸣谢



- [jarrett]: https://github.com/jarrett-au/douban2noition

- [Geetheshe]: https://github.com/Geetheshe/DoubanMovieListBackUpToNotion

