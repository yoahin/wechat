#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import argparse
import os.path
import os

#TODO
# [X] pass the article dir as a tempalte folder
# [X] test if include will work
parser = argparse.ArgumentParser(description='Generate template html for posts')

# 1st arg: article dir where children templates stored
parser.add_argument('-d', '--article-directory',
                    help='article dir of children templates')
# 2nd arg: base templates dir
parser.add_argument('-t', '--templates-directory',
                    default=os.abspath('./templates'),
                    help='Templates direcotry (default: ./templates')
args = parser.parse_args()

project_dir = '${PROJECTS_HOME}/posts/wechat/'
article_dir = os.path.join(project_dir, str(argv[1]))
# each time article part template will be updated: 1.html, 2.html, 3.html, ... and so on
article_part = str(argv[2])


file_loader = FileSystemLoader(
        ['templates/te-templates',
         'templates/dict-templates',
         'templates/twitter-templates',
         article_dir])
env = Environment(loader=file_loader)

print(env.list_templates(extensions=["html"]))
    #TODO
    # figure out how this 'parent' argument works
    # and let the lookup order goes deeper
    # FileSystemLoader will also load templates in subdirectories
    # but it recognizes those templates as they are: /path/to/template
    # if parent='string' given, then it would be string/path/to/template
    # which in turn leads TemplateNotFound error

    # better to keep templates in the same folder at the same depth
template = env.get_template(article_part)

output = template.render(title='Tiktok')
print('output is', output, sep='\n')
#with open('test.html', 'w', encoding='utf-8') as test:
#    test.write(output)
