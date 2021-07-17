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

if sensenum:
	# syn_blocks consist of 1) def & e.g.s, 2) synonyms, 3) related words
	syn_blocks = etree.xpath(f'//span[@class="sn sense-{sensenum}"]/following-sibling::*')
else:
	raise SystemExit('No sense number given; Execution terminated')


def get_def_eg(node):
	# XPath must be like the one in a filesystem
	# Those in the middle of a path cannot be skipped over
	sense = node.xpath('./text()')[0].strip(' ,\n\t')
	egs = []
	egs_num = len(node.xpath('./ul'))
	for ith in range(egs_num):
		eg = ''.join(node.xpath(f'./ul[{ith+1}]/li/span/text() | ./ul[{ith+1}]/li/span/em/text()'))
		egs.append(eg)

	return sense, egs

# syns blocks are all the same
def get_synonyms(node):
	'''Get the list of syns or related words'''
	syns_nds = node.xpath('./div/ul/li')
	syns_num = len(syns_nds)
	syns_lst = []
	syns_usg = {}
	syns_vrt = {}

	for ith in range(syns_num):
		# NOTE: current node now is a single <li> element!
		# if it is a synonym, add it to the list
		if syns_nds[ith].xpath('./a/text()'):
			syns_lst.append(syns_nds[ith].xpath('./a/text()')[0])
		# if it is a usage tag, add it to usg dict with its order number
		elif syns_nds[ith].xpath('./span[@class="wsls"]'):
			syns_usg[ith] = '[' + syns_nds[ith].xpath('./span[@class="wsls"]/text()')[0] + ']'
		# # if it is a word variant, add it to vrt dict with its order number
		elif syns_nds[ith].xpath('./span[@class="wvrs"]/span'):
			syns_vrt[ith] = '(' \
						+ syns_nds[ith].xpath('./span[@class="wvrs"]/span[1]/text()')[0]\
						+ ' '\
						+ syns_nds[ith].xpath('./span[@class="wvrs"]/span[2]/a/text()')[0]\
						+ ')'
	 

	return syns_lst, syns_usg, syns_vrt


if __name__ == '__main__':
	if not output:
		#print(syn_blocks)
		#sense, egs = def_eg(syn_blocks[0])
		lst, usg, vrt = get_synonyms(syn_blocks[1])
		print(lst,usg,vrt,sep='\n')
