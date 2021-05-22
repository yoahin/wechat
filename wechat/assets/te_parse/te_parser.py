#! \usr\bin\env python3
# -*- coding: utf-8 -*-

# The TE Parser
# This files includes all three parts: header, body, img
# from the *te* package 

from html.parser import HTMLParser
import requests
from pathlib import Path


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


class GetBody(HTMLParser):
    def __init__(self):
    # Since Python 3, we need to call the __init__() function 
    # of the parent class
        # use this counter as a switch
        self.para_counter = 0
        self.nested_counter = 0
        # List is not empty to let the first dropped letter
        # have an achor to attach itself to
        # otherwise it will try to find list[-1] of an empty list
        self.paras = ['']
        super().__init__()
        self.reset()
    
    # Defining what the methods should output when called by HTMLParser.
    def handle_starttag(self, tag, attrs):
        # small and em tag to handle a few TE styled words
        # span tag to specifically handle the EOF, a square
        if tag != 'p' and tag != 'small' and tag != 'em' \
        and tag != 'span' and tag != 'strong':
            return
        if self.para_counter:
            # because in the case of TE 
            # only small or em or span or strong will be nested
            self.nested_counter += 1
            return
        # only parse body paras:
        for attr, val in attrs:
            if attr == 'class' and 'article__body-text' in val:
                break
        else:
            return
        # if encounter any body para, count 1
        self.para_counter = 1
    
    def handle_endtag(self, tag):
        # if such p contains child tag
        # the child tag's data will be read first
        # before the counter reduces to 0 again
        if tag == 'p' and self.para_counter and self.nested_counter:
            self.nested_counter -= 1
            self.para_counter -= 1
        elif tag == 'p' and self.para_counter and not self.nested_counter:
            self.para_counter -= 1

    def handle_data(self, data):
        if self.para_counter and not self.nested_counter:
            self.paras.append(data)
        elif self.nested_counter:
            self.paras[-1] = self.paras[-1] + data

    def get_data(self):
        return self.paras 


    def process_data(self):
        for i in range(len(self.paras)):
            if len(self.paras[i]) == 1 and i < len(self.paras) - 1:
                self.paras[i+1] =  '<span class="te-drop">' \
                                + self.paras[i] \
                                + '</span>' \
                                + self.paras[i+1]
            else:
                self.paras[i] = '<p class="tel-p">' + self.paras[i] + '</p>'
        return self.paras



class GetImage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.recording = 0
        self.img_srcs = []

    def handle_starttag(self, tag, attrs):
        # outmost layer
        if (tag == 'div' and ('class', 'article__lead-image') in attrs) or \
            (tag == 'figure' and ('data-image-nozoom', 'true') in attrs):
            self.recording += 1
        # enter the outmost layer
        # and count the second
        if self.recording:
            if (tag == 'div' and ('itemprop', 'image') in attrs):
                self.recording += 1
        # reach the innermost layer: img
        if self.recording == 2 and tag == 'img':
            for attr, val in attrs:
                if attr == 'src':
                    self.img_srcs.append(val)

    def handle_endtag(self, tag):
        if (tag == 'div' or tag =='figure') and self.recording:
            self.recording -= 1 

    def get_result(self):
        print(self.img_srcs)
        return

    def download_imgs(self, path):
        # mkdir img/ if it does not exist yet
        if not Path(path).exists(): Path(path).mkdir()

        with requests.Session() as s: 
            for i in range(len(self.img_srcs)):
                r = s.get(self.img_srcs[i]) 
                if i == 0: 
                    with open(f'{path}/header-img.{self.img_srcs[i][-3:]}', 'wb') as img: 
                        img.write(r.content)
                else:
                    with open(f'{path}/body-{i}.{self.img_srcs[i][-3:]}', 'wb') as img:
                            img.write(r.content)

