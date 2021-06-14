#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script will use base templates under ./templates and 
children templates in various dirs under ../wechat/*/ to
create the html files used for wechat posts.
"""

from jinja2 import Environment, FileSystemLoader
import argparse
from os.path import abspath, basename, join

#TODO
# [X] pass the article dir as a tempalte folder
# [X] test if include will work
parser = argparse.ArgumentParser(description='Create template htmls for posts')

# read the doc: https://docs.python.org/dev/library/argparse.html#dest
# 1st arg: article dir where children templates stored
parser.add_argument('-d', '--article-directory',
                    metavar='/path/to/article/dir',
                    default=abspath('.'),
                    help='article dir of children templates; defaults to cwd')
# 2nd arg: base templates dir
parser.add_argument('-t', '--templates-directory',
                    metavar='/path/to/templates',
                    default=abspath('./templates'),
                    help='Templates direcotry (default: ./templates)')
# 3rd arg: template part to be posted
parser.add_argument('-p', '--post-part',
                    metavar='/path/to/article/part',
                    default=abspath('./1.html'),
                    help='The article part to be posted; (default: ./1.html)')
args = parser.parse_args()

# abspath is platform independent
article_dir = abspath(args.article_directory)

# each time article part template will be updated: 1.html, 2.html, 3.html, ...
article_part = args.post_part


file_loader = FileSystemLoader(
        ['templates/te-templates',
         'templates/dict-templates',
         'templates/twitter-templates',
         article_dir])
env = Environment(loader=file_loader)

print(env.list_templates(extensions=["html"]))
# TODO
# figure out how this 'parent' argument works
# and let the lookup order goes deeper
# FileSystemLoader will also load templates in subdirectories
# but it recognizes those templates as they are: /path/to/template
# if parent='string' given, then it would be string/path/to/template
# which in turn leads to TemplateNotFound error

# better to keep templates in the same folder at the same depth
template = env.get_template('new-yorker-base.html')

output = template.render(title=f'{basename(article_dir) + article_part[0:-5]}')
print('output is', output, sep='\n')
#with open('test.html', 'w', encoding='utf-8') as test:
#    test.write(output)
