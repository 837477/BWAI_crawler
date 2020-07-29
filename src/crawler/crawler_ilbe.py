import time
import requests
from bs4 import BeautifulSoup

from crawler.crawler import request_crawler
from etc.variable import url_list
from model.BWAI_model import BWAI__posts, BWAI__variable

def run_ilbe():
    target_url = []
    for url in url_list:
        if url['title'][:4] == "ilbe":
            target_url.append(url['url'])


    for url in target_url:
        crawler = request_crawler(url)

        Flag = True
        while Flag:
            try:
                page = crawler.getPage()
            except:
                continue

            try:
                target_list = page.find("div", {"class": "board-list"}).find("ul").findAll("a", {"class": "subject", "style": None})
            except:
                continue
            
            if not target_list:
                break
            
            for url in target_list:
                try:
                    document = {}

                    # url 등록
                    document['url'] = crawler.getDomain() + url['href']

                    # 타깃 접속!
                    target = request_crawler(document['url'])
                    page = target.getPage()
                    time.sleep(2)
                    
                    # 제목 크롤
                    title = page.find("div", {"class": "post-wrap"}).find("div", {"class": "post-header"}).find("a").get_text(" ", strip = True)
                    document['title'] = title
                    print("URL: " + document['url'])
                    print("제목: " + title)

                    # 본문 크롤
                    document['post'] = []
                    post = page.find("div", {"class": "post-wrap"}).find("div", {"class": "post-content"}).findAll("p")
                    if post:
                        for p in post:
                            text = p.get_text(" ", strip = True)
                            if len(text) > 0:
                                document['post'].append(text)
                            
                    else:
                        text = page.find("div", {"class": "post-wrap"}).find("div", {"class": "post-content"}).get_text(" ", strip = True)
                        if len(text) > 0:
                            document['post'].append(text)

                    document['join_post'] = ' '.join(document['post'])

                    print("본문: " + document['join_post'])
                    print("===================================================")
                except:
                    continue

                BWAI__posts(target.getDB()).insert__one(document)
            
            crawler.changePage(1)
