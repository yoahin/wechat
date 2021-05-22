#!/usr/bin/env python3

# scrape an article page from TE 1843 long reads
# and collect its header content

from html.parser import HTMLParser


class GetHeader(HTMLParser):
    def __init__(self):
        self.record_subheadline = 0
        self.record_headline = 0
        self.record_description = 0
        self.header = []
        # in Python 2
        # super(Parser, self).__init__()
        # in Python 3, though Python 2 style also applies 
        super().__init__()
        #self.reset()

    def handle_starttag(self, tag, attrs):
        #TODO
        # rewrite this part to improve performance
        for attr, val in attrs:
            # count subheadline, headline, description respectively
            if tag == 'span' and attr == 'class' and val == 'article__subheadline':
                self.record_subheadline += 1
            elif attr == 'class' and val == 'article__headline':
                self.record_headline += 1
            elif attr == 'class' and val == 'article__description':
                self.record_description += 1
        else:
            return


    def handle_endtag(self, tag):
        if tag == 'span' and self.record_subheadline:
            self.record_subheadline -= 1
        elif tag == 'span' and self.record_headline:
            self.record_headline -= 1
        elif tag == 'p' and self.record_description:
            self.record_description -= 1

    def handle_data(self, data):
        if self.record_headline or \
           self.record_subheadline or \
           self.record_description:
            self.header.append(data)

    def get_header(self):
        return self.header

    def process_header(self):
        if len(self.header) == 3:
            self.header[0] = '<h2 class="tel-col">' + self.header[0] + '</h2>'
            self.header[1] = '<h1 class="tel-title">' + self.header[1] + '</h1>'
            self.header[2] = '<h3 class="tel-subtitle">' + self.header[2] + '</h3>'
            return self.header
        else:
            print('Header has more than 3 elements.')

if __name__ == '__main__':
    from sys import argv
    from urllib.request import urlopen

    url = urlopen(argv[1])
    html = url.read().decode('UTF-8')
    url.close()
    test = GetHeader()
    test.feed(html)
    print(test.process_header())
