# -*- coding=utf-8 -*-

"""
This script, as a module, will try to scrape the header, body, and footer
from a New Yorker online article page.
If it is used as a script, it will use the first argument
passed on command line to the script.
"""

import argparse
import requests
import os
import os.path
from lxml import html


def cmd_arg_parser():
    parser = argparse.ArgumentParser(description='Parse user input url')
    # 1st arg: destination/directory
    parser.add_argument('-d', '--destination',
                        nargs='?', const='.', default='.',
                        help='destination of the output file (default: cwd)')

    # 2nd arg: url
    parser.add_argument('url', help='url of online article to be scrpaed')

    args = parser.parse_args()
    if os.path.exists(args.destination):
        print(f'Html files will be stored in directory {os.path.abspath(args.destination)}')
    else:
        os.mkdir(args.destination)
        print(f'{args.destination} does not exist yet, creating it ...')
        print(f'Html files will be stored in directory {args.destination}')
    return args


class Article():
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

    def get_tree(self):
        return self.tree

    class Header():
        """
        Header class focuses on fetch the article's header parts:
        title, subtitle, byline, publshing date, column name and so on.
        """

        def __init__(self, tree):
            """
            Initialize the nested class to use the tree
            """
            self.tree = tree

        def get_h1(self):
            """
            Get the headline #1 text and mark it up accrodingly
            Headline #1 is the article title.
            """
            self.h1 = self.tree.xpath('//h1[\
                                        contains(@class, "content-header__row")\
                                        ]/text()')[0]
            return '<h1>' + self.h1 + '</h1>'

        def get_h2(self):
            """
            Get the headline #2 text and mark it up accrodingly
            Headline #2 is the article's subtile.
            """
            self.h2 = self.tree.xpath('//div[\
                                        contains(@class, "content-header__dek")\
                                        ]/text()')[0]
            return '<h2>' + self.h2 + '</h2>'

        def get_column(self):
            """
            Get the column name and mark it up accrodingly
            Column name, for example, DAILY COMMENT.
            """
            self.column = self.tree.xpath('//a[\
                                        contains(@class, "rubric__link")\
                                        ]/span[1]/text()')[0]
            return '<h3>' + self.column.upper() + '</h3>'

        def get_byline(self):
            """
            Get the byline text and mark it up accrodingly
            Byline, for example, By Peter Hessle.
            """
            self.preamble = self.tree.xpath('//span[\
                                            contains(@class, "byline__preamble")\
                                            ]/text()')[0]
            # TNY splits byline name into weird two parts
            self.byline_part1 = self.tree.xpath('//a[\
                                        contains(@class, "byline__name-link")\
                                        ]/text()')[0]
            self.byline_part2 = self.tree.xpath('//span[\
                                    contains(@class, "link__last-letter-spacing")\
                                        ]/text()')[0]
            return '<h4>' + self.preamble\
                          + self.byline_part1\
                          + self.byline_part2\
                          + '</h4>'

        def get_pubdate(self):
            """
            Ge the publishing date of the article and mark it up with h5.
            """
            self.pubdate = self.tree.xpath('//time[\
                                contains(@class, "content-header__publish-date")\
                                ]/text()')[0]
            return '<h5>' + self.pubdate + '</h5>'

        def get_caption(self):
            self.caption_text = '<h2 class="cap_text">'\
                + self.tree.xpath('//span[contains(@class, "caption__text")]/text()')[0]\
                + '</h2>'
            self.caption_credit = '<span class="cap_credit">'\
                + self.tree.xpath('//span[contains(@class, "caption__credit")]/text()')[0]\
                + '</span>'
            return self.caption_text, self.caption_credit

    class Body():
        """
        Get all the body paragraphs and mark them up with p tag.
        """

        def __init__(self, tree):
            self.tree = tree

        def get_paras(self):
            """
            Get all breaking points of the paragraphs.
            Such as a tags, em tags and so on.
            """
            # TODO: handle the nested tags such as <a>, <em>.
            self.first_para = self.tree.xpath('//p[contains(@class, "has-dropcap")]')
            self.paras_raw = self.first_para + self.tree.xpath('//p[@class="paywall"]')
            self.para_num = len(self.paras_raw)
            self.paras_text = {}
            self.para_a_or_em = {}
            # self.para_ems = {}

            for i in range(self.para_num):
                self.paras_text[str(i)] = self.paras_raw[i].xpath('./text()')
                _a_or_em_text = self.paras_raw[i].xpath(
                        './a[@class="external-link"]/text() | ./em/text()'
                        )

                # Filter out empty nodes
                if _a_or_em_text:
                    self.para_a_or_em[str(i)] = _a_or_em_text

            for p_num, nodes in self.para_a_or_em.items():
                # if a paragraph has a or em tags
                if p_num in self.paras_text:
                    # concatenate the a/em_text to the text before/after
                    # the breaking point so paras' number remains the same
                    for i in range(len(nodes)):
                        self.paras_text[p_num][i] = self.paras_text[p_num][i] + nodes[i]

            # Mark up all the paragraphs
            for p in self.paras_text:
                self.paras_text[p] = '<p>' + ''.join(self.paras_text[p]) + '</p>'

            return self.paras_text


if __name__ == '__main__':
    args = cmd_arg_parser()
    article_url = args.url
    article_title = article_url[article_url.rfind('/') + 1:].replace('-', ' ')
    print(f'Article tilte is {article_title}')

    dest = args.destination

    # Create an article instance and scrape the html tree
    article = Article(article_url)
    html_tree = article.get_tree()

    # Get the header parts by create a header instance and using the tree
    header = article.Header(html_tree)
    h1 = header.get_h1()
    h2 = header.get_h2()
    column = header.get_column()
    byline = header.get_byline()
    publishing_date = header.get_pubdate()
    cap_text, cap_credit = header.get_caption()
    #print(f'Article Title is {h1}')
    #print(f'Article Subtitle is {h2}')
    #print(f'Article column is {column}')
    #print(f'Article byline is {byline}')
    #print(f'Article was published online on {publishing_date}')
    #print(f'Article caption text is {cap_text}')
    #print(f'Article caption text is {cap_credit}')

    with open(os.path.join(dest, 'header.html'), 'w', encoding='utf-8') as f:
        f.write(h1+'\n')
        f.write(h2+'\n')
        f.write(column+'\n')
        f.write(byline+'\n')
        f.write(publishing_date+'\n')
        f.write(cap_text+'\n')
        f.write(cap_credit+'\n')



    # Get the body paras by creating a body instance
    body = article.Body(html_tree)
    paras = body.get_paras()

    with open(os.path.join(dest, 'body.html'), 'w', encoding='utf-8') as f:
        for p in paras:
            f.write(paras[p] + '\n')

    print(paras)
