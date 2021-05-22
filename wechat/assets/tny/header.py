#!/usr/bin/env python3
# get tny header part of personal history articel page
# skip header img which is better to be extracted with other cartoons


from urllib.request import urlopen
from html.parser import HTMLParser

class GetHeader(HTMLParser):
    def __init__(self):
        self.counter = 0
        self.nested = 0
        self.content = {}
        super().__init__()

    def handle_starttag(self, tag, attrs):
        # column and issue number
        if tag == 'a' and ('class' in attrs[0] and 'rubric__link' in attrs[0][1]):
            self.counter += 1
        elif self.counter and tag == 'span':
            self.nested += 1
        #if tag == 'a':
        #    print(attrs)

        # headline
        elif tag == 'h1':
            self.counter += 1
        # subheadline
        elif tag == 'div' and ('class', 'content-header__row content-header__dek') in attrs:
            self.counter += 1
        # online publication date
        # guess: this appears as static data, appearing before the author was inserted by js
        # though author's name ends up preceding the time
        elif tag == 'time':
            self.counter += 1
        # byline name
        # somehow the class attr is not included in the scraped result
        # and it appears *after* the time tag in the scraped result (but *before* if using inspector)
        # perhaps it was added by js when rendering the site page
        elif tag == 'a' and ('href' in attrs[0] and 'contributors' in attrs[0][1]):
            self.counter += 1

    def handle_data(self, data):
        # data that has to be extracted by using the parents tag 
        # in which the data nested in
        if self.counter and self.nested:
            if 'column' not in self.content:
                self.content['column'] = data
            elif 'issue' not in self.content:
                self.content['issue'] = data
        # data that can be extracted directly from the tag containing it 
        if self.counter and not self.nested:
            if 'h1' not in self.content:
                self.content['h1'] = data
            elif 'h2' not in self.content:
                self.content['h2'] = data
            elif 'time' not in self.content:
                self.content['time'] = data
            elif 'author' not in self.content:
                self.content['author'] = data

    def handle_endtag(self, tag):
        if self.counter and self.nested:
            self.nested -= 1
        elif self.counter and not self.nested:
            self.counter -= 1

    def GetContent(self):
        return self.content
    

if __name__ == '__main__':
    url = urlopen('https://www.newyorker.com/magazine/2019/11/25/my-life-as-a-child-chef')
    html = url.read().decode('UTF-8')
    url.close()

    test = GetHeader()
    test.feed(html)
    print(test.GetContent())
