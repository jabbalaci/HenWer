#!/usr/bin/env python

import os
import re
import urlparse
from urllib import urlopen
from bs4 import BeautifulSoup

site = 'http://fetish.iiichan.net/'       # site's address
name = 'One Thread, One Fetish'
referer = None

def myComp(x, y):
    "x and y are tuples"
    def getNum(t):
        return int( re.search(r'\((\d+)\)$', t[1]).group(1) )
    return cmp(getNum(x), getNum(y))

def addBaseUrl(elem):
    "elem is a 2-element list"
    elem[0] = urlparse.urljoin(site, elem[0])
    return elem

def get_result():
    soup = BeautifulSoup(urlopen(site).read())

    list = []   # list of 2-element lists
    for a in soup.findAll('a'):
        if a.has_key('href'):
            link = a
            result = re.search(r'<a .*href="(.*?)".*>(.*)</a>', str(link))
            if result:
                href = result.group(1)
                desc = result.group(2)
                if href.startswith('/res/'):
                    res = re.search(r'\d{1,2}:.*\(\d+\)$', desc)
                    if res:
                        list.append( [href, desc] )   # we insert 2-element lists

    #print list
    list.sort(myComp, reverse=True)
    list = map(addBaseUrl, list)

    li = ['MAIN PAGE']   # the list is initialized with the main page
    urls = [site]        # main page of the site
    for link in list:
        #print link[0], "->", link[1]
        urls.append(link[0])
        li.append(link[1])
        # debug
        #get_relative_save_dir("fetish", link[1])
    # add main page to the end too
    li.append('MAIN PAGE')
    urls.append(site)

    return (li, urls)


def gather_gallery_list():
    #li = []     # list of galleries (names)
    #urls = []   # URLs of the galleries
    return get_result()

def get_referer():
    return referer

def get_relative_save_dir(part1, part2):
    part2 = part2.lower()
    result = re.search(r'.*:(.*)\(.*\)', part2)
    if result:
        part2 = result.group(1)
    part2 = re.sub(r'&#\d+;', '', part2)
    part2 = re.sub(r' ', '_', part2)
    part2 = re.sub(r'\W', '', part2)
    part2 = re.sub(r'_+', '_', part2)
    part2 = re.sub(r'_+', '_', part2)
    part2 = re.sub(r'^_+', '', re.sub(r'_+$', '', part2))
    path = os.path.join(part1.lower(), part2)
    #print ">>>", path
    return path

#############################################################################

if __name__ == "__main__":
    print gather_gallery_list()
