'''
    Created on 10/22/2017
    @author Yupeng Gu
    reference: https://www.dataquest.io/blog/web-scraping-tutorial-python/
'''

import time
from datetime import datetime
from Log import *
import sys

max_count = 50


# send email
def push(all_papers, recipient = None):

    print len(all_papers)
    return

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
    if recipient is None:
        send_mail('Daily Paper Summary: {}'.format(today), c)
    else:
        send_mail('Daily Paper Summary: {}'.format(today), c, recipient)
    print 'Email sent!'


def main():
    all_papers = []
    import KDD_17 
    KDD_17.crawl(all_papers, max_count)

    push(all_papers)

if __name__ == '__main__':
    main()


