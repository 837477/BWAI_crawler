import requests
from pymongo import *
from bs4 import BeautifulSoup

from etc.secret_info import MONGO_HOST, MONGO_ID, MONGO_PW, MONGO_DB_NAME

header = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
            AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
            "Accept":"text/html,application/xhtml+xml,application/xml;\
            q=0.9,imgwebp,*/*;q=0.8"
        }

class request_crawler:
    # 생성자
    def __init__(self, url):
        super(request_crawler, self).__init__()
        # Crawler
        self.url = url 
        self.domain = self.url.split('/')[0] + '//' + self.url.split('/')[2]
        self.target = self.url + '2'
        self.url_list = []
        self.page_num = 2
        # DB Client    
        self.db_client = MongoClient('mongodb://%s:%s@%s' %(MONGO_ID, MONGO_PW, MONGO_HOST))
        self.db = self.db_client['BWAI']

    # return db
    def getDB(self):
        return self.db

    # 페이지 넘버 이동
    def changePage(self, num):
        self.page_num += num
        self.target = self.url + str(self.page_num)

    # 페이지 가져오기
    def getPage(self):
        driver = requests.get(self.target, verify = False, headers = header).text
        page = BeautifulSoup(driver, 'html.parser')
        return page

    # 페이지 리스트 생성
    def makePagelist(self, sub_url_list, num):
        if num <= len(self.url_list):
            return False
        elif sub_url_list:
            for url in sub_url_list:
                self.url_list.append(self.domain + url['href'])
            return True
        else:
            return False

    # 도메인 추출
    def getDomain(self):
        return self.domain

    # target url_list 반환
    def getURLlist(self):
        return self.url_list

    # DB cursor 반환
    def getDB(self):
        return self.db

    # 소멸자
    def __del__(self):
        self.db_client.close()
