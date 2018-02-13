# -*- coding: utf-8 -*-
# @Author: Alex
# @Date:   2018-01-20 22:18:08
# @Last Modified by:   Anthorty
# @Last Modified time: 2018-02-13 22:19:34
# Version: 0.0.1

import requests
import re
import os
import json
import lxml
import http.cookiejar
from bs4 import BeautifulSoup

post_url = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
           'Referer': 'https://www.pixiv.net/'}

start_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                 'Referer': ''}
prepare_url = set()
front_url = "https://www.pixiv.net/"
multi_front_url = "https://www.pixiv.net"
detail_url = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id="

setDate = input("请输入爬取日期，格式为YYYYMMDD，如20180101，最新日期为昨天\n")
setList = input("设置爬取榜单，0.日榜 1.周榜 2.月榜 3.男性喜爱\n")
setMaxPage = input("设置爬取页数，最大不超过10页\n")

# 设置爬取榜单，0.日榜 1.周榜 2.月榜 3.男性喜爱
rankList = ["daily", "weekly", "monthly", "male"] 
referInfo = ["day", "week", "month", "male"]
setRankList = rankList[int(setList)] 
setRef = referInfo[int(setList)] 

listDate = f"&date={setDate}"
begin_url = f"https://www.pixiv.net/ranking.php?mode={setRankList}&ref=rn-h-{setRef}-3" + listDate
origin_url = {}
next_pages_url = []
multipic_url = set()
really_multipic_url = {}

class pixiv_spider():
    def __init__(self):
        self.session = requests.session()
        self.headers = headers
        self.session.headers = self.headers
        self.session.cookies = http.cookiejar.LWPCookieJar(filename = "pixiv_cookies")
        try:
            self.session.cookies.load(filename = "pixiv_cookies", ignore_discard = True)
            print("成功读取cookies")
        except Exception as e:
            print("找不到cookies文件，无法加载")

        self.params = {
            "lang":"zh",
            "source":"pc",
            "view_type":"page",
            "ref":"wwwtop_accounts_index"
        }

        self.datas = {
            'pixiv_id': '',
            'password': '',
            'captcha': '',
            'g_recaptcha_response': '',
            'post_key': "",
            'source': 'pc',
            'ref': 'wwwtop_accounts_index',
            'return_to': 'http://www.pixiv.net/',
        }

    def get_postkey(self):
        r = self.session.get(post_url, params = self.params)
        soup = BeautifulSoup(r.content, 'lxml')
        post_key = soup.find_all('input')[0]['value']
        self.datas['post_key'] = post_key

    def check_login(self):
        check_url = "https://www.pixiv.net/setting_user.php"
        login_code = self.session.get(check_url, allow_redirects = False).status_code
        if login_code == 200:
            return True
        else:
            return False

    def login_in(self, username, password):
        self.get_postkey()
        self.datas['pixiv_id'] = username
        self.datas['password'] = password
        post_data = self.session.post(post_url, data = self.datas)
        self.session.cookies.save(ignore_discard = True, ignore_expires = True)

    def start_spider(self, start_url, maxPage): #控制爬取页数，最大不超过10页
        start_headers['Referer'] = 'https://www.pixiv.net'
        self.session.headers = start_headers
        rankListInfo = self.session.get(start_url)
        rankListObj = BeautifulSoup(rankListInfo.content, 'lxml')
        links = rankListObj.find_all('a','title')
        verified_key = rankListObj.find('input', attrs={'name':'tt'})['value']
        for link in links:
            prepare_url.add(front_url+link['href'])
        for page in range(2, maxPage): 
            next_pages_url.append(f'https://www.pixiv.net/ranking.php?mode={setRankList}&p={str(page)}&format=json&tt={verified_key}')

    def parse_json(self, pages_url):
        next_pages_info = self.session.get(pages_url)
        next_pages_json = json.loads(next_pages_info.text)
        for next_url in next_pages_json.get('contents'):
            prepare_url.add(detail_url+str(next_url.get('illust_id')))                   

    def on_spider(self, page_url):
        start_headers['Referer'] = begin_url
        self.session.headers = start_headers
        detail_info = self.session.get(page_url)
        detail_infoObj = BeautifulSoup(detail_info.content, 'lxml')
        check_url = detail_infoObj.find('img', 'original-image')
        if check_url != None:
            download_url = detail_infoObj.find('img', 'original-image')['data-src']
            origin_url[download_url] = page_url
        elif check_url == None:
            multipic_url.add(page_url)


    def parse_multipic(self, page_url):
        start_headers['Referer'] = begin_url
        self.session.headers = start_headers
        detail_info = self.session.get(page_url)
        detail_infoObj = BeautifulSoup(detail_info.content, 'lxml')
        really_url = multi_front_url + detail_infoObj.find('a', 'read-more js-click-trackable')['href']

        start_headers['Referer'] = page_url
        self.session.headers = start_headers
        multipic_detail_info = self.session.get(really_url)
        multipic_detail_infoObj = BeautifulSoup(multipic_detail_info.content, 'lxml')
        really_multipic_url[really_url] = []
        multipicUrlList = multipic_detail_infoObj.find_all('img', 'image')
        for multipicUrl in multipicUrlList:
            really_multipic_url[really_url].append(multipicUrl['data-src'])

    def download_pic(self, download_link, page_url, file_path = f'Picture/{setRankList}/{setDate}'):
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_format = os.path.splitext(download_link)[1]
        file_name = re.findall(r'\d{7,10}', page_url)[0]
        file_all_name = file_name + file_format
        file_final_name = os.path.join(file_path, file_all_name)
        start_headers['Referer'] = page_url
        self.session.headers = start_headers
        try:
            download_pic = self.session.get(download_link)
            with open(file_final_name, 'wb') as f:
                f.write(download_pic.content)
        except Exception as e:
            print("Download Error!", e)

    def download_multipic(self, download_link, page_url , file_path = f'Picture/multipic/{setRankList}/{setDate}'):
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_format = os.path.splitext(download_link)[1]
        file_name = re.findall(r'\d{7,10}_\w\d{1,2}', download_link)[0]
        file_all_name = file_name + file_format
        file_final_name = os.path.join(file_path, file_all_name)
        start_headers['Referer'] = page_url
        self.session.headers = start_headers
        try:
            download_pic = self.session.get(download_link)
            with open(file_final_name, 'wb') as f:
                f.write(download_pic.content)
        except Exception as e:
            print("Download Error!", e)

if __name__ == '__main__':
    count = 0
    multi_count = 0
    spider = pixiv_spider()
    if spider.check_login():
        print("已登录")
    else:
        username = input("请输入帐号")
        password = input("请输入密码")
        spider.login_in(username, password)

    spider.start_spider(begin_url, int(setMaxPage) + 1)

    for next_page in next_pages_url:
        spider.parse_json(next_page)

    for url in prepare_url:
        spider.on_spider(url)

    for multiUrl in multipic_url:
        spider.parse_multipic(multiUrl)

    for downloadUrl,pageUrl in origin_url.items():
        count += 1
        spider.download_pic(downloadUrl, pageUrl)
        print(f"正在下载第{count}张单图")

    for page_url, multipic_urlList in really_multipic_url.items():
        for multipicUrl in multipic_urlList:
            multi_count += 1
            spider.download_multipic(multipicUrl, page_url)
            print(f"正在下载第{multi_count}张多图")


    print(f"共下载{count}张单图，{multi_count}张多图")