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


def get_target():
    '''
    Get the target url or local file from command line args
    '''
    parser = argparse.ArgumentParser(description='Fetch synonyms of a ginve word from Merriam-Webster')

    # 1st arg: Sense num of a given word

    parser.add_argument('-s', '--sense-num',
        default=None,
        help='Sense number of the word (Default: none)')

    # 2nd arg: Merriam-Webster word page url
    parser.add_argument('-u', '--url', help='URL of the word\' dictionary page')

    # 3rd arg: Local file
    parser.add_argument('-f', '--file', help='Local file path')

    # 4th arg: Output to stdout or a file
    parser.add_argument('-o', '--output', help='Output to a file instead of stdout')

    args = parser.parse_args()

    # get the values of args
    sensenum = args.sense_num
    url = args.url

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            raw_html = f.read()
    else:
        raw_html = args.file
    output = args.output
    return sensenum, url, raw_html, output


# Get the blocks for a specific sense
def get_blocks(etree, sense_num=None):
    if sense_num:
        # syn_blocks consist of 1) def & e.g.s, 2) synonyms, 3) related words
        syn_blocks = etree.xpath(f'//span[@class="sn sense-{sense_num}"]/following-sibling::*')

    else:
        syn_blocks = etree.xpath('//div[@class="sense no-subnum"]/child::*')
        # raise SystemExit('No sense number given; Execution terminated')

    return syn_blocks


# syns blocks are very similar:
# - Synonyms --> type:syn
# - Related Words --> type: rel
# - Phrases Synonyms --> type: phr
# - Near Antonyms --> type: ant


def get_synonyms(blocks, type='syn'):
    '''Get the list of syns or related words'''

    for block in blocks:
        if block.xpath(f'//span[contains(@class, "{type}-list")]'):
            node = block.xpath(f'//span[contains(@class, "{type}-list")]')[0]
            break
        # print('Found syn block')

    # get the list content header
    syns_hed = node.xpath('./div[@class="thes-list-header"]/p[@class="function-label"]/text()')[0] +\
        node.xpath('./div[@class="thes-list-header"]/p[@class="function-label"]/em/text()')[0]

    # get the list
    syns_nds = node.xpath('./div[@class="thes-list-content synonyms_list"]/ul/li')
    syns_num = len(syns_nds)
    syns_lst = []    # list of synonyms
    syns_usg = {}    # word usage, e.g. slang, colloquial
    syns_vrt = {}    # variant: also YYY


    for ith in range(syns_num):
        # NOTE: current node now is a single <li> element!
        # if it is a synonym, add it to the list
        if syns_nds[ith].xpath('./a/text()'):
            syns_lst.append(syns_nds[ith].xpath('./a/text()')[0])

        # if it is a usage tag, add it to usg dict with its order number
        elif syns_nds[ith].xpath('./span[@class="wsls"]'):
            syns_usg[ith] = '[' + syns_nds[ith].xpath('./span[@class="wsls"]/text()')[0] + ']'

        # if it is a word variant, add it to vrt dict with its order number
        elif syns_nds[ith].xpath('./span[@class="wvrs"]/span'):
            syns_vrt[ith] = '(' \
                 + syns_nds[ith].xpath('./span[@class="wvrs"]/span[1]/text()')[0]\
                 + ' '\
                 + syns_nds[ith].xpath('./span[@class="wvrs"]/span[2]/a/text()')[0]\
                 + ')'

    return syns_hed, syns_lst, syns_usg, syns_vrt


def get_related(node):
    pass


def get_antonyms(node):
    pass


if __name__ == '__main__':
    # Get needed elements
    sensenum, url, raw_html, output = get_target()

    # Detect raw html based on args passed
    if url:
        raw_content = requests.get(url).text

    if raw_html:
        raw_content = raw_html

    etree = html.fromstring(raw_content)
    syn_blocks = get_blocks(etree, sensenum)

    # thes list keywords: 'syn', 'rel', 'phrase', 'near', 'ant'
    if not output:
        print(syn_blocks)

        hed, lst, usg, vrt = get_synonyms(syn_blocks, 'rel')
        print(hed, lst, usg, vrt, sep='\n')
        # print(get_sense())
    if output:
        pass
