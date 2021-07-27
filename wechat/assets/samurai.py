# -*- coding: utf-8 -*-
'''
This scirpt depends on mw-fetch.py and mwth-fetch.py;
It will use the fetched content to generate
the needed word templates
'''

# standard or 3rd party libs
import requests
from lxml import html
from os.path import join

# my own module
from fetchers.mwth import get_target, get_blocks, get_synonyms

if __name__ == '__main__':
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
