from bs4 import BeautifulSoup
import urllib2
import download as dl
import codecs
import re
import glob, os
def get_page(page_num):
    from_path = "http://www.javbus.com/ja/actresses/%d" % page_num
    to_path = "actress_page/%d" % page_num
    dl.download_url(from_path, to_path)
for pageId in range(656, 657):
    get_page(pageId)
