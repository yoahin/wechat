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
from os.path import exists, join
from os import environ, mkdir
# my own module
from fetchers.mwth import get_target, get_entry,\
    get_nodes, get_sense, get_egs, get_synonyms

if __name__ == '__main__':
    sensenum, url, raw_html, output = get_target()
    # Detect raw html based on args passed
    if url:
        raw_content = requests.get(url).text

    if raw_html:
        raw_content = raw_html
    etree = html.fromstring(raw_content)
    syn_nodes = get_nodes(etree, sensenum)

    entry = {'sense-num': f'{sensenum}'}
    entry['entry'], entry['entry_nums'] = get_entry(etree)

    file_loader = FileSystemLoader(['templates/dicts', 'templates/icons'])
    env = Environment(loader=file_loader)
    templates = env.list_templates(extensions=['j2'])
    template = env.get_template('webster/th-base.j2')
    ROOT_DIR = join(environ['HOME'], 'projects', 'posts', 'wechat', 'vocab')
    if not exists(ROOT_DIR):
        mkdir(ROOT_DIR)

    # make each single node an key-value item in word
    for ntype, node in syn_nodes.items():
        if ntype == 'dt':
            entry['def'] = get_sense(node)
            entry['egs'] = get_egs(node)
            print(entry)
            continue
        else:
            hed, lst = get_synonyms(node)
            if 'Synonyms' in hed:
                entry['syn'] = lst
            elif 'Related' in hed:
                entry['rel'] = lst
            elif 'Near' in hed:
                entry['near'] = lst
            elif 'Near' not in hed and 'Antonyms' in hed:
                entry['ant'] = lst
            elif 'Phrases' in hed:
                entry['phrase'] = lst
        # print(hed, lst, sep='\n')
    # print(word)
    if not output:
        print(entry)
    if output:
        content = template.render(word=entry)
        with open(join(ROOT_DIR, output+sensenum+'.html'), 'w', encoding='utf-8') as op:
            op.write(content)
