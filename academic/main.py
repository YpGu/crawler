'''
    Created on 10/22/2017
    @author Yupeng Gu
    reference: https://www.dataquest.io/blog/web-scraping-tutorial-python/
'''

import requests
import bs4
from bs4 import BeautifulSoup
import time
from datetime import datetime
from Log import *
import sys

source_page = 'http://www.kdd.org/kdd2017/accepted-papers'
recipient = 'gyp7364@gmail.com'
max_count = 50


class Entity:
    def __init__(self, title, url, authors):
        self.title = title
        self.url = url
        self.authors = authors


# send email
def push(all_papers, recipient):
    if len(all_papers) == 0:
        print 'No events available, try again tomorrow!'

    c = ''
    for p in all_papers:
        c = c + '<a href = {}>{}</a>'.format(p.url, p.title) + '<br>'
        c = c + p.authors + '<br>'
        c = c + '<br>'
    c = c.encode('ascii', 'ignore')

    sys.path.append('../../mail/')
    from sendmail import send_mail 
    today = datetime.now().strftime("%m/%d/%Y")
    send_mail('Daily Paper Summary: {}'.format(today), c, recipient)
    print 'Email sent!'


def main():
    all_papers = []; count = 0
    while True:
        if count >= max_count:
            push(all_papers, recipient)
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
                '''
                an example of p:

                <tr><td><strong><span style="color:rgb(10,160,110)"><a href="http://www.kdd.org/kdd2017/papers/view/randomization-or-condensation-linear-cost-matrix-sketching-via-cascaded-com">Randomization or Condensation?: Linear-Cost Matrix Sketching Via Cascaded Compression Sampling</a></span></strong><br/><small>Author(s): Kai Zhang (Lawrence Berkeley National Laboratories);Chuanren Liu (Drexel University);Jie Zhang (Fudan University);Hui Xiong (Rutgers University);Eric Xing (Carneigie Mellon University);Jieping Ye (University of Michigan)</small></td></tr>
                '''
                if type(p) is bs4.element.Tag:
                    url_title = p.find('a')
                    title = url_title.get_text()
                    url = url_title['href']
                    authors = p.find('small').get_text().split('Author(s): ')[-1]

                    e = Entity(title, url, authors)
                    all_papers.append(e)
                    count += 1

                if count >= max_count: 
                    push(all_papers, recipient)
                    return

        break

if __name__ == '__main__':
    main()


