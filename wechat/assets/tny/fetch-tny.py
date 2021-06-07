# -*- coding=utf-8 -*-

"""
This script, as a module, will try to scrape the header, body, and footer
from a New Yorker online article page.
If it is used as a script, it will ask the user for a New Yorker url instead.
"""

import argparse
import requests
from lxml import html


def cmd_arg_parser():
    parser = argparse.ArgumentParser(description='Parse user input url')
    # 1st arg: url
    parser.add_argument('url', help='url of online article to be scrpaed')
    args = parser.parse_args()
    return args


class Header():
    """
    Accept an url as it argument and return the text nodes of the header part.
    The header part can be further divided into headlines 1-5, byline, column."
    """

    def __init__(self, url):
        # TODECIDE: must have a url as its initial arg?
        """
        Initialize the object so that it will return a parsed html tree.
        """
        self.url = url
        self.content = requests.get(self.url).text
        self.tree = html.fromstring(self.content)

    def get_h1(self):
        """
        Get the headline #1 text and mark it up accrodingly
        """
        return self.tree.xpath('//h1[\
                                    contains(@class, "content-header__row")\
                                    ]/text()')

    def get_h2():
        pass

    def get_h3():
        pass

    def get_h4():
        pass

    def get_h5():
        pass

    def get_column():
        pass

    def get_byline():
        pass


if __name__ == '__main__':
    args = cmd_arg_parser()
    article_url = args.url
    article_title = article_url[article_url.rfind('/') + 1:].replace('-', ' ')
    print(f'Article tilte is {article_title}')

    # Create an header instance
    header = Header(article_url)
    h1 = header.get_h1()
    print(f'Article Header is {h1}')
