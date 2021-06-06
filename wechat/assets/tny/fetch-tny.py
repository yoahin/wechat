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
        get the headline #1 text and mark it up accrodingly
        """

        pass

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
