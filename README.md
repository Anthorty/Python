## Pixiv爬虫

##### 请先确认网络能正常打开P站！！！
##### 请先确认网络能正常打开P站！！！
##### 请先确认网络能正常打开P站！！！

##### 需要Python3.6及以上才能正常运行

这是一个单线程的P站爬虫，没加入多线程，所以爬取速度有点慢，个人使用应该没有问题。
爬虫没加入`sleep`，请不要短时间多次爬取，否则可能暂时ban了ip。

爬虫使用了`requests , BeautifulSoup , lxml`，如果不能正常运行，请检查是否安装所需的第三方库。

本爬虫特点：
1. 支持指定爬取日期
2. 支持指定爬取榜单
3. 支持指定爬取页数
4. 下载后的图片按照文件夹分类，文件名以P站ID命名

不足之处：
1. 没有加入多线程功能
2. 没有针对网络连接问题进行优化
3. 没有本地化存储未爬取链接（减轻服务器负担）



## Pixiv Spider

##### Please confirm your network can open pixiv first!!!
##### Please confirm your network can open pixiv first!!!
##### Please confirm your network can open pixiv first!!!

##### NEED Python3.6 and above to run normally

This is a single-threaded spider,so the speed not fast,personal use should be ok.
Please don't crawling frequent in short time,it will ban your ip temporary.

Before use please install`requests , BeautifulSoup , lxml`.

Feature:
1. can set crawling date
2. can set crawling list
3. can set crawling page
4. downloaded picture sort by list type,filename is picture id

Shortcoming:
1. no multiprocess function
2. no optimization for network connectivity issues
3. no localised storage for uncrawled links (reducing server load) 