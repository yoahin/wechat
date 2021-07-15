# -*- coding: utf-8 -*-

'''
This scirpt will scrape Merriam-Webster thesaurus page
and get all the synonyms of a given entry.
The syns will be stored in a list
'''

import argparse
import requests
from os.path import abspath, exists, join
from lxml import html

parser = argparse.ArgumentParser(description='Fetch synonyms of a ginve word from Merriam-Webster')

# 1st arg: Merriam-Webster word page url
parser.add_argument('-u', '--url', 
										help='URL of a word page')

# 2nd arg: 
parser.add_argument('-o', '--out-put',
										help='Output to a file instead of stdout')

args = parser.parse_args()


# get the values of args
url = args.url
output = args.out_put

raw_content = requests.get(url).text
etree = html.fromstring(raw_content)

# TODO: fix bug -- group the fetched words according the original page
syns = etree.xpath('//span[contains(@class, "re-list")]\
	/div[contains(@class, "synonyms_list")]\
	/ul[contains(@class, "mw-list")]/li/a/text()')

if not output:
	print(syns)
