import requests
from bs4 import BeautifulSoup

from crawler.crawler import request_crawler
from etc.variable import url_list
from model.BWAI_model import BWAI__posts

def run_ilbe():
    target_url = []
    for url in url_list:
        if url['title'][:4] == "ilbe":
            target_url.append(url['url'])


    for url in target_url:
        ilbe_crawler = request_crawler(url)

        Flag = True
        while Flag:
            page = ilbe_crawler.getPage()
            target_list = page.find("div", {"class": "board-list"}).find("ul").findAll("a", {"class": "subject", "style": None})
            Flag = ilbe_crawler.makePagelist(target_list, 2000000)
            ilbe_crawler.changePage(1)
            break
        
        for url in ilbe_crawler.url_list:
            document = {}

            # url 등록
            document['url'] = url

            # 타깃 접속!
            target = request_crawler(url)
            page = target.getPage()
            
            # 제목 크롤
            title = page.find("div", {"class": "post-wrap"}).find("div", {"class": "post-header"}).find("a").get_text(" ", strip = True)
            document['title'] = title
            print("URL: " + url)
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

            BWAI__posts(target.getDB()).insert__one(document)