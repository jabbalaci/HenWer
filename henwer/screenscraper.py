#!/usr/bin/env python

import re
import urllib.parse
from urllib.request import urlopen

from bs4 import BeautifulSoup


class ExtractImageURLs:
    """This is a simple image URL extractor"""

    def remove_duplicates(self, li):
        """remove duplicates from a list by keeping the order"""
        dict = {}
        copy = []
        for e in li:
            if e not in dict:
                copy.append(e)
                dict[e] = 1
        return copy

    def get_image_urls(self, baseUrl):
        """extract URLs from a given address"""
        text = urlopen(baseUrl).read()
        soup = BeautifulSoup(text)

        li = []
        for a in soup.findAll("a"):
            if "href" in a:
                link = a
                result = re.search(r'<a .*href="(.*?)".*>(.*)</a>', str(link))
                if result:
                    href = result.group(1)
                    # r = re.search(r'\.jpg$', href.lower())
                    r = re.search(r"\.(png|jpg|gif)$", href.lower())
                    if r:
                        li.append(href)

        li = [urllib.parse.urljoin(baseUrl, e) for e in li]
        return self.remove_duplicates(li)


#############################################################################

if __name__ == "__main__":
    ex = ExtractImageURLs()
    li = ex.get_image_urls("http://fetish.iiichan.net/")
    print(li)
    print(len(li))
