import requests
import bs4
from bs4 import BeautifulSoup
import time
from datetime import datetime
from Log import *
import sys
from Entity import Entity

source_page = 'http://www.kdd.org/kdd2017/accepted-papers'

def crawl(all_papers, max_count):
    while True:
        if len(all_papers) >= max_count:
            return

        try:
            page = requests.get(source_page)
        except requests.exceptions.Timeout:
            time.sleep(60)
            continue
        except requests.exceptions.RequestException as e:
            write_log('./error.log', e, datetime.now())
            time.sleep(60)
            continue

        if page.status_code != 200:
            time.sleep(60)
            continue 

        soup = BeautifulSoup(page.content, 'html.parser')

        res = soup.find_all('table', class_ = 'table table-hover table-striped table-bordered')
        for r in res: 
            #print type(r)
            papers = list(r.children)[3]
            for p in papers:
                if type(p) is bs4.element.Tag:
                    url_title = p.find('a')
                    title = url_title.get_text()
                    url = url_title['href']
                    authors = p.find('small').get_text().split('Author(s): ')[-1]

                    e = Entity(title, url, authors)
                    all_papers.append(e)

                if len(all_papers) >= max_count: 
                    return

        break

