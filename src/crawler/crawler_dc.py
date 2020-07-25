import time
import requests
from bs4 import BeautifulSoup

from crawler.crawler import request_crawler
from etc.variable import url_list
from model.BWAI_model import BWAI__posts, BWAI__variable

def run_dc():
    target_url = []
    for url in url_list:
        if url['title'][:2] == "dc":
            target_url.append(url['url'])


    for url in target_url:
        crawler = request_crawler(url)

        Flag = True
        while Flag:
            try:
                page = crawler.getPage()
            except:
                continue
            time.sleep(3)
            try:
                target = page.find("tbody").findAll("td", {"class": "ub-word"})
            except:
                continue
            target_list = []
            for t in target:
                try:
                    temp = {}
                    temp['href'] = t.find("a")['href']
                    target_list.append(temp)
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
                    time.sleep(3)
                    
                    # 제목 크롤
                    title = page.find("h3", {"class": "title"}).find("span", {"class": "title_subject"}).get_text(" ", strip = True)
                    document['title'] = title
                    print("URL: " + document['url'])
                    print("제목: " + title)

                    # 본문 크롤
                    document['post'] = []

                    post = page.find("div", {"class": "writing_view_box"})
                    if post:
                        document['post'].append(post.get_text(" ", strip = True))
                    
                    document['join_post'] = ' '.join(document['post'])
                    print(document['post'])
                    print("본문: " + document['join_post'])
                    print("===================================================")
                except:
                    continue

                BWAI__posts(target.getDB()).insert__one(document)
            
            crawler.changePage(1)
