#!\usr\bin\env python3
# -*- coding: utf-8 -*-
# Parse New Yorker's article pages and get the images
# This single module exists solely for getting images
# it also acts as the prototype of the same class in the main 
# `telongreads.py` file

import requests
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import urlopen


class GetImages(HTMLParser):
    def __init__(self):
        super().__init__()
        self.fig_recording = 0
        self.img_recording = 0
        self.img_counter = 0
        self.caption_text_recording = 0
        self.caption_credit_recording = 0
        self.img_srcs = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'figure':
            self.fig_recording += 1
            return 
        if self.fig_recording:
            if tag == 'img' and ('class', 'responsive-image__image') in attrs:
                self.img_recording += 1
                self.img_counter += 1
		# suppose all img tags are like: <img class="xxx" alt="yyy" src="url">
                self.img_srcs[self.img_counter] = {'src': attrs[2][1]}
                return
        #for attr, val in attrs:
        #    if tag == 'span' and self.fig_recording:
        #        print('attrs: ', attrs)

        if tag == 'span' and self.fig_recording:
            # caption text span
            # attrs: [('class', 'classa classb classc ...')]
            if 'class' in attrs[0] and 'caption__text' in attrs[0][1]:
                self.caption_text_recording += 1
                return

            ## caption credit span
            elif 'class' in attrs[0] and 'caption__credit' in attrs[0][1]:
                self.caption_credit_recording += 1
                return

    def handle_data(self, data):
        if self.caption_text_recording:
            self.img_srcs[self.img_counter].update([('caption_text', data)])
        elif self.caption_credit_recording:
            self.img_srcs[self.img_counter].update([('caption_credit', data)])
    
    def handle_endtag(self, tag):
        if tag == 'figure' and self.fig_recording:
            self.fig_recording -= 1
        if tag == 'img' and self.img_recording:
            self.img_recording -= 1
        elif tag == 'span' and self.caption_text_recording:
            self.caption_text_recording -= 1
        elif tag == 'span' and self.caption_credit_recording:
            self.caption_credit_recording -= 1

    def get_content(self):
        return self.img_srcs

    def download_imgs(self, path):
        # mkdir img/ if it does not exist yet
        if not Path(path).exists(): Path(path).mkdir()

        with requests.Session() as s:
            for i in list(self.img_srcs):
                r = s.get(self.img_srcs[i]['src'])
                with open(f'{path}/img-{i}.{self.img_srcs[i]["src"][-3:]}', 'wb') as img:
                    img.write(r.content)

if __name__ == '__main__':
    url = urlopen('https://www.newyorker.com/magazine/2019/11/25/my-life-as-a-child-chef')
    html = url.read().decode('UTF-8')
    url.close()

    test = GetImages()
    test.feed(html)
    print(test.get_content())
    test.download_imgs('img')
