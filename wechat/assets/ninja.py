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
                    metavar='ARTICLE_DIR_BASENAME',
                    default=basename('.'),
                    help='Basename of the article directory where children \
                          templates are stored (e.g. peace); defaults to\
                          $(basename "."). See --post-part option for more\
                          information on how args will be used to set the \
                          needed paths.')
# 2nd arg: article part to be posted
# NOTE: git-tracking current.html so that each time on different machine
# its content along with header, dicts or so will be populated to num.html
parser.add_argument('-p', '--post-part',
                    nargs=2,
                    metavar=('NEWS_SRC', 'PART_NUM'),
                    default=(basename('.'), '1'),
                    help='The article part to be posted;\
                         NOTE: this option is used to create output file under\
                         ROOT_DIR/NEWS_SRC/ARTICLE_DIR_BASENAME. ROOT_DIR \
                         will always be automatically set to the following:\
                         $HOME/projects/posts/wechat. The output file will \
                         be named based on PART_NUM given, for example: 2.html\
                          (i.e.part 2 of an article). NEWS_SRC defaults to\
                         the basename of current directory, PART_NUM to 1.')
# 3rd arg: base template to be used
parser.add_argument('-b', '--base-template',
                    default='new-yorker-base.html',
                    help='The base template; (default: new-yorker-base.html)')

# parse all args
args = parser.parse_args()

# each time article part template will be updated: 1.html, 2.html, 3.html, ...
article_source = abspath(join('..', args.post_part[0]))
article_dir = abspath(join('..', article_source, args.article_directory))
part_num = args.post_part[1]
base_template = args.base_template

file_loader = FileSystemLoader(
        ['templates',
         'templates/te-templates',
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

# NOTE: template file should be a variable
# template should be the one you want to get from output
# i.e. the one that extends the base
template = env.get_template('current.html')

output = template.render(
        title=f'{args.article_directory}-{part_num}')
with open(join(article_dir, part_num+'.html'), 'w', encoding='utf-8') as f:
    f.write(output)

