# -*- coding: utf-8 -*-
'''
This scirpt depends on two fetchers: mw.py and mwth.py;
It will use the fetched content to generate
the needed word/synonyms templates.
'''

# standard or 3rd party libs
import requests
from jinja2 import Environment, FileSystemLoader
from lxml import html
from os.path import join

# my own module
from fetchers.mwth import get_target, get_entry, get_nodes, get_sense, get_egs, get_synonyms

if __name__ == '__main__':
    sensenum, url, raw_html, output = get_target()
    # Detect raw html based on args passed
    if url:
        raw_content = requests.get(url).text

    if raw_html:
        raw_content = raw_html

    etree = html.fromstring(raw_content)
    syn_nodes = get_nodes(etree, sensenum)

    word = {'sense-num': f'{sensenum}'}
    word['entry'], word['entry_nums'] = get_entry(etree)
    # thes list keywords: 'syn', 'rel', 'phrase', 'near', 'ant'
    if not output:
        for ntype, node in syn_nodes.items():
            if ntype == 'dt':
                word['def'] = get_sense(node)
                word['egs'] = get_egs(node)
                print(word)
                continue
            else:
                hed, lst = get_synonyms(node)
                #if usg:
                #    for pst in usg.keys():
                #        lst[pst - 1] = lst[pst - 1] +  usg[pst]
                #if vrt:
                #    for pst in vrt.keys():
                #        lst[pst - 1] = lst[pst - 1] + vrt[pst]
                print(hed, lst, sep='\n')
    if output:
        pass
