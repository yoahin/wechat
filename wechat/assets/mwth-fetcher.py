# -*- coding: utf-8 -*-

'''
This scirpt will scrape Merriam-Webster thesaurus page
and get all the synonyms of a given entry.
The syns will be stored in a list
'''

import argparse
import requests
from lxml import html
from os.path import abspath, exists, join


parser = argparse.ArgumentParser(description='Fetch synonyms of a ginve word from Merriam-Webster')

# 1st arg: Sense num of a given word

parser.add_argument('-s', '--sense-num', help="Sense number of the word (Default: none)")

# 2nd arg: Merriam-Webster word page url
parser.add_argument('-u', '--url', help='URL of the word\' dictionary page')

# 3rd arg: 
parser.add_argument('-o', '--out-put', help='Output to a file instead of stdout')

args = parser.parse_args()


# get the values of args
sensenum = args.sense_num
url = args.url
output = args.out_put

raw_content = requests.get(url).text
etree = html.fromstring(raw_content)

# TODO: fix bug -- group the fetched words according the original page
if sensenum:
	# syn_blocks consist of 1) def & e.g.s, 2) synonyms, 3) related words
	syn_blocks = etree.xpath(f'//span[contains(@class, "sense-{sensenum}")]/following-sibling::*')
else:
	raise SystemExit('No sense number given; Execution terminated')


if not output:
	print(syn_blocks)
