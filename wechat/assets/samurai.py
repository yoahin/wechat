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
from fetchers.mwth import get_target, get_nodes, get_sense, get_egs, get_synonyms

if __name__ == '__main__':
    sensenum, url, raw_html, output = get_target()
    # Detect raw html based on args passed
    if url:
        raw_content = requests.get(url).text

    if raw_html:
        raw_content = raw_html

    etree = html.fromstring(raw_content)
    syn_nodes = get_nodes(etree, sensenum)

    # thes list keywords: 'syn', 'rel', 'phrase', 'near', 'ant'
    if not output:
        for ntype, node in syn_nodes.items():
            if ntype == 'dt':
                sns = get_sense(node)
                egs = get_egs(node)
                print(f'Sense: {sns}')
                for eg in egs:
                    print(f'E.g.: {eg}')
                continue
            else:
                hed, lst, usg, vrt = get_synonyms(node)
                print( hed, lst, usg, vrt, sep='\n')
        # print(get_sense())
    if output:
        pass
