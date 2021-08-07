# -*- coding: utf-8 -*-

'''
This scirpt will scrape Merriam-Webster thesaurus page
and get all the synonyms of a given entry.
The syns will be stored in a list
'''

import argparse
import requests
from lxml import html


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


def get_entry(etree):
    '''
    Get the entry word and entry numbers, e.g.:
    Entry: a_word
    Entry_nums: (Entry x of y)
    '''
    header_node = etree.xpath('//div[@class="row vg-header"]')[0]
    entry = header_node.xpath('./div/h2/em/text()')[0]
    entry_nums = header_node.xpath('./div/p[@class="entryNumbers"]/text()')[0].rstrip(' \t')
    return entry, entry_nums


def get_nodes(etree, sense_num=None):
    '''Get the target synonyms span nodes such as:
    1) defination (or sense)
    2) example(s)
    3) synonyms
    4) related words
    5) near antonyms
    6) phrases synonymous
    '''
    if sense_num:
        nodes = etree.xpath(f'//span[@class="sn sense-{sense_num}"]/following-sibling::*')

    else:
        nodes = etree.xpath('//div[@class="sense no-subnum"]/*')
        # raise SystemExit('No sense number given; Execution terminated')

    # preprocess nodes so that the node list becomes
    # a hash table of nodes: syn_nodes
    syn_nodes = {}
    for node in nodes:
        # The following xpaths are identical:
        # self::span[@class="dt "]
        # //span/descendent-or-self::span[@class="dt "]
        # Xpath always returns a list
        nclasses = node.xpath('self::span/@class')[0].split()
        # print(nclasses)
        for ntype in ['dt', 'syn-list', 'rel-list', 'ant-list', 'near-list', 'phrase-list']:
            if ntype in nclasses:
                syn_nodes[ntype] = node
                break

    print(syn_nodes)
    return syn_nodes


def get_sense(node):
    '''Get the specific sense'''
    sense = node.xpath('./text()')[0].strip(' ,\n\t')
    return sense


def get_egs(node):
    '''Get all the examples listed under a specific sense.'''
    # Xpath must be like the one of a filesystem
    # Those in the middle of a path cannot be skipped over
    egs = []
    egs_num = len(node.xpath('./ul'))
    for ith in range(egs_num):
        # xpath counting is 1-based
        eg = ''.join(node.xpath(f'./ul[{ith+1}]/li/span/text()'))
        egs.append(eg)

    return egs

# syns blocks are very similar:
# - Synonyms --> type:syn
# - Related Words --> type: rel
# - Phrases Synonyms --> type: phr
# - Near Antonyms --> type: ant


def get_synonyms(node):
    '''Get the list of syns or related words'''

    # get the list content header
    # for debugging purposes only
    syns_hed = node.xpath('./div[@class="thes-list-header"]/p[@class="function-label"]/text()')[0] +\
        node.xpath('./div[@class="thes-list-header"]/p[@class="function-label"]/em/text()')[0]

    # get the list
    syns_nds = node.xpath('./div[@class="thes-list-content synonyms_list"]/ul/li')
    syns_num = len(syns_nds)
    syns_lst = []    # list of synonyms
    #syns_usg = {}    # word usage, e.g. slang, colloquial
    #syns_vrt = {}    # variant: also YYY

    for ith in range(syns_num):
        # NOTE: current node now is a single <li> element!
        # if it is a synonym, add it to the list
        if syns_nds[ith].xpath('./a/text()'):
            syns_lst.append(syns_nds[ith].xpath('./a/text()')[0])

        # if it is a usage tag, concat it to the previous element which it belongs to
        elif syns_nds[ith].xpath('./span[@class="wsls"]'):
            syns_lst[-1] = syns_lst[-1] + ' <span class="mwth-syns-label">[<em>'\
                + syns_nds[ith].xpath('./span[@class="wsls"]/text()')[0]\
                + '</em></span>]'
        # if it is a word variant, also concat it to the previous element
        elif syns_nds[ith].xpath('./span[@class="wvrs"]/span'):
            syns_lst[-1] = syns_lst[-1] + ' <span class="mwth-syns-label">(<em>' \
                 + syns_nds[ith].xpath('./span[@class="wvrs"]/span[1]/text()')[0]\
                 + '</em></span> '\
                 + syns_nds[ith].xpath('./span[@class="wvrs"]/span[2]/a/text()')[0]\
                 + '<span class="mwth-syns-label">)</span>'

    return syns_hed, syns_lst


def get_related(node):
    pass


def get_antonyms(node):
    pass


if __name__ == '__main__':
    # Get needed elements
    sensenum, url, raw_html, output = get_target()
    print(sensenum)
    # Detect raw html based on args passed
    if url:
        raw_content = requests.get(url).text

    if raw_html:
        raw_content = raw_html

    etree = html.fromstring(raw_content)
    syn_nodes = get_nodes(etree, sensenum)

    # thes list keywords: 'syn', 'rel', 'phrase', 'near', 'ant'
    if not output:

        # skip the first 'dt' node
        for ntype, node in syn_nodes.items():
            if ntype == 'dt':
                sns = get_sense(node)
                egs = get_egs(node)
                continue
            else:
                hed, lst = get_synonyms(node)
            print(sns, egs, hed, lst, sep='\n')
    if output:
        pass
