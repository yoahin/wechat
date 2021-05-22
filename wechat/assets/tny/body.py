#!/usr/bin/env python3
# get tny body paragraphs of personal history articel page
# skip header img which is better to be extracted with other cartoons


from urllib.request import urlopen
from html.parser import HTMLParser

class GetBodyParas(HTMLParser):
    def __init__(self):
        #self.counter = 0     # general counter
        self.article = 0     # like above, to count nested tags
        self.pnumber = 0     # count number of paras
        self.dcounter = 0    # count number of paras with dropcap
        self.pcounter = 0    # count number of normal paras
        self.quoteblock = 0  # count quoteblock
        self.footer = 0      # count footer
        self.content = {}    # get paragraphs raw data
        self.paragraphs = {} # formatted paragraphs (i.e. surrounded by html tags)
        super().__init__()

    def handle_starttag(self, tag, attrs):
        """Get only the paragraphs inside the <main> or <article> tag"""
        # mark the entry of article part
        if tag == 'article' and ('class', 'article main-content') in attrs:
            self.article += 1
        # count paras with drop cap
        elif tag == 'p' and self.article and \
            ('class', 'has-dropcap has-dropcap__lead-standard-heading') in attrs:
            #self.counter += 1 
            self.pnumber += 1
            self.dcounter += 1
            self.content[self.pnumber] = {'has_dropcap': []}
        # counter normal para
        elif tag == 'p' and self.article and not attrs and not self.quoteblock:
            self.pcounter += 1
            self.pnumber += 1
            self.content[self.pnumber] = {'normal_para': []}
        # counter paras in quoteblock
        elif tag == 'div' and ('class', 'blockquote-embed__content') in attrs:
            self.pnumber += 1
            self.quoteblock += 1
            self.content[self.pnumber] = {'quoteblock': []}
        elif tag == 'footer' and ('content-footer__magazine-disclaimer' in attrs[0][1]):
            self.footer += 1
            self.pnumber += 1
            self.content[self.pnumber] = {'footer': []}

    def handle_data(self, data):
        """divide paras into two groups:
            1. has_dropcap;
            2. normal_para
            appending to a list and joining its element later will avoid
            list index out of range error -- if first elemnet of a list 
            happens to be in a nested tag"""
        # paras with drop cap
        if self.dcounter:
            self.content[self.pnumber]['has_dropcap'].append(data) 
        # normal paras 
        elif self.pcounter:
            self.content[self.pnumber]['normal_para'].append(data)
        # quoteblock paras
        elif self.quoteblock:
            self.content[self.pnumber]['quoteblock'].append(data)
        elif self.footer:
            self.content[self.pnumber]['footer'].append(data)



    def handle_endtag(self, tag):
        if tag == 'p' and self.dcounter:
            #self.counter -= 1
            self.dcounter -= 1
        elif tag == 'p' and self.pcounter:
            self.pcounter -= 1
        elif tag == 'div' and self.quoteblock:
            self.quoteblock -= 1
        elif tag == 'article' and self.article:
            self.article -= 1
        elif tag == 'footer' and self.footer:
            self.footer -= 1

    def get_content(self):
        for para_number in list(self.content):
            if self.content[para_number].get('has_dropcap', 0):
               self.paragraphs[para_number] = '<p class="first-para">' \
                                            + ''.join(self.content[para_number]['has_dropcap']) \
                                            + '</p>'
            elif self.content[para_number].get('normal_para', 0):
               self.paragraphs[para_number] = '<p>' \
                                            + ''.join(self.content[para_number]['normal_para']) \
                                            + '</p>'
            elif self.content[para_number].get('quoteblock', 0):
               self.paragraphs[para_number] = '<p class="quotes">' \
                                            + ''.join(self.content[para_number]['quoteblock']) \
                                            + '</p>'
            elif self.content[para_number].get('footer', 0):
               self.paragraphs[para_number] = '<p class="footer">' \
                                            + ''.join(self.content[para_number]['footer']) \
                                            + '</p>'
        return self.paragraphs 


if __name__ == '__main__':
    url = urlopen('https://www.newyorker.com/magazine/2019/11/25/my-life-as-a-child-chef')
    html = url.read().decode('UTF-8')
    url.close()

    test = GetBodyParas()
    test.feed(html)
    print(test.get_content())



