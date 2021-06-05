# -*- coding=utf-8 -*-

# This script will parse URL and path passed on command line
# and output the scraped content to a html file stored in the path
# Author： Errelin

import os.path
import os
import sys
import argparse
from urllib.request import urlopen


# 3rd party (my own) module
import tny.header
import te_parse

os_name = sys.platform

if os_name.startswith('win32'):
    ROOT_DIR = os.path.join(os.environ['USERPROFILE'], \
                        'projects', \
                        'posts', \
                        'wechat')
else:
    ROOT_DIR = os.path.join(os.environ['HOME'], \
                        'projects', \
                        'posts', \
                        'wechat')

parser = argparse.ArgumentParser(description='Fetch the content of an online article')

# command line args
parser.add_argument('-d', '--directory', \
                    nargs='?', const='.', default=os.getcwd(), \
                    help='destination where the output will be stored')
parser.add_argument('-u', '--url', help='the url of which to be scraped')


args = parser.parse_args()

# NOTE: must use long form for the attr name
article_url = args.url

# extract article title from the url
article_title = article_url[article_url.rfind('/') + 1:]
print('Article title is', article_title.replace('-', ' '))

# write to the file named article_title.html under the dest passed
target_folder = args.directory
if target_folder != None:
    target_file = os.path.join(ROOT_DIR, target_folder, article_title + '.html')
# defaults to None; save to current directory then
else:
    target_file = os.path.join(args.directory, article_title + '.html')

with open(target_file, 'w', encoding='utf-8') as f:
        url_obj = urlopen(article_url)
        html = url_obj.read().decode('UTF-8')
        url_obj.close()

        header = tny.header.GetHeader()
        header.feed(html)
        print(header.GetContent())
        #TODO: write to the file instead of standard output 
        f.write('this is a simple test')