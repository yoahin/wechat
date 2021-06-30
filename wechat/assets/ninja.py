#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script will use base templates under ./templates and
children templates in various dirs under ../wechat/*/ to
create the html files used for wechat posts.
"""

from jinja2 import Environment, FileSystemLoader
import argparse
from os.path import exists, expanduser, join
from os import makedirs

# TODO
# [X] swap 1st and 2nd args
# [ ] test if modularized dict templates will work

parser = argparse.ArgumentParser(
        description='Create html templates for wechat posts')

# read the doc: https://docs.python.org/dev/library/argparse.html#dest
# 1st arg: article dir where children templates stored
parser.add_argument('-s', '--news-source',
                    metavar='NEWS_SRC',
                    default='NONE',
                    help='Basename of the news source directory where \
                          different article posts are stored. For exmaple, \
                          "Economist". If the source name contains spaces, \
                          it should be quoted like "New York Times". If no \
                          arg passed, defaults to "NONE". See --post-part \
                          option for more information on how args are used \
                          to set the needed paths.')
# 2nd arg: article part to be posted
# NOTE: git-tracking current.html so that each time on different machine
# its content along with header, dicts or so will be populated to num.html
parser.add_argument('-p', '--post-part',
                    nargs=2,
                    metavar=('TITLE_KEYWORD', 'PART_NUM'),
                    default=('nil', '1'),
                    help='The article part to be posted;\
                         NOTE: this option is used to create output file under\
                         ROOT_DIR/NEWS_SRC/TITLE_KEYWORD. ROOT_DIR\
                         will always be automatically set to the following:\
                         $HOME/projects/posts/wechat. The output file will\
                         be named based on PART_NUM given, for example: 2.html\
                          (i.e.part 2 of the article). TITLE_KEYWORD defaults\
                         to "nil"; PART_NUM defaults to 1. Example:\
                         passing "cyber 1" will make TITLE_KEYWORD "cyber" and\
                         PART_NUM "1".')
# 3rd arg: base template to be used
parser.add_argument('-t', '--base-template',
                    default='example-base.html',
                    help='The base template file name, with extension.\
                          Default: example-base.html')

# parse all args
args = parser.parse_args()

ROOT_DIR = join(expanduser('~'), 'projects', 'posts', 'wechat')

# each time article part template will be updated: 1.html, 2.html, 3.html, ...
news_source = args.news_source
article_dir = join(ROOT_DIR, news_source, args.post_part[0])
if not exists(article_dir):
    makedirs(article_dir)
part_num = args.post_part[1]

# NOTE: sub-directories will be counted relatively.
# For example, templates/economist/te-color.htm' will be recognized as
# /economist/te-color.html. The template root dir will be stripped.
file_loader = FileSystemLoader(
        [
         'templates',
         article_dir
         ])
env = Environment(loader=file_loader)
templates = env.list_templates(extensions=["html"])
print('Templates are as follows: ')
print(templates)
print(f'Found {len(templates)} templates in total.')
# NOTE
# FileSystemLoader will also load templates in subdirectories
# but it recognizes those templates as they are: /path/to/template

# NOTE:
# The final template to be rendered should be the one that extends/includes
# other templates, rather than the base templates themselves, like the "main"
# function in C programs. Here it is named "current.html".

# The "current.html" template is placed in the same dir as the parts of an
# artcile, for example, "New Yorker/involution/current.html".

# It indicates the most recent changes for a specific article and will
# not be tracked in the git tree, as it is clearly not necessary to do so.
# Similarly, the "notes.html" under the same dir will not be tracked either.
# Both will be moved over to the new article's dir once they are done with
# the current one.

template = env.get_template('current.html')

output = template.render(
        title=f'{args.post_part[0]}-{part_num}',
        base=args.base_template
        )
with open(join(article_dir, part_num+'.html'), 'w', encoding='utf-8') as f:
    f.write(output)
