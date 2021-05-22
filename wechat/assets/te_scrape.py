#!/usr/bin/env python3

# Parse te 1843 article pages:
# headlines, paragraphs, imgs

from urllib.request import urlopen
from . te_parse import te_parser 
from sys import argv
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import os.path
from pathlib import Path

project_dir = '/home/leon/projects/gitty/wechat/'
article_url = argv[1]
article_src = str(argv[2]) + '/' 
article_til = str(argv[3]) 
article_dir = os.path.join(project_dir, article_src, article_til)
if not Path(article_dir).exists(): Path(article_dir).mkdir()
print(article_dir)


try:
    # prepare html to feed
    url = urlopen(article_url)
    html = url.read().decode('UTF-8')
    url.close()
    

    # prepare the article parser
    te_article_header = te_parser.GetHeader()
    te_article_body = te_parser.GetBody()
    te_article_img = te_parser.GetImage()

    # scrape needed parts 
    te_article_header.feed(html)
    te_article_body.feed(html)
    te_article_img.feed(html)
    
    # create header template
    # header
    headers = te_article_header.process_header()  # a list
    with open(article_dir + '/header.html', 'w', encoding='utf-8') as h:
        for header in headers:
            h.write(header+'\n')


    # body
    paras =  te_article_body.process_data()  # a list
    with open(article_dir + '/body.html', 'w', encoding='utf-8') as b:
        for para in paras:
            b.write(para+'\n\n')

    # img
    te_article_img.download_imgs(article_dir + '/img')



except Exception as error:
    logger.exception(error)
