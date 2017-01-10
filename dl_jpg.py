#!/usr/bin/env python3
# Scan folder Sorted/
# if /A/ACD/ACD-001/ACD-001.jpg doesn't exists
# download from internet

import os
import re
import sys
import ntpath
import scandir
import errno
# Python 3
import urllib.request
from bs4 import BeautifulSoup
import download as dl 
import html

def get_content(path):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    content = ""
    print("urlopen: {}".format(path))
    try:
        request = urllib.request.Request(path, None, hdr)
        content = u''.join(urllib.request.urlopen(request).read().decode('utf-8'))
    except Exception as e:
        print("Exception for {} reason: {}".format(path, str(e)))
        pass
    return content
def get_javlib_link(content, product_id):
    soup = BeautifulSoup(content)
    #print("soup.len = {}".format(len(soup)))
    link = soup.find('img', {'id': 'video_jacket_img'})
    if link == None:
        print('Cannot find jpg javlib link from "{}", abort...'.format(product_id))
        return None 
    return link['src']
def get_javbus_link(content, product_id):
    soup = BeautifulSoup(content)
    link = soup.find('a', {'class': 'bigImage'})
    print("========= {} ==========".format(link))
    if link == None:
        print('Cannot find jpg javbus link from "{}", abort...'.format(product_id))
        return None 
    return link['href']
        
def scan_jpg(path):
    if not os.path.exists(path):
        print('Path not exists: {}'.format(path))
        return
    for entry in scandir.scandir(path):
        ep = entry.path
        if entry.is_dir(follow_symlinks=False):
            yield from scan_jpg(ep)  # see below for Python 2.x
        else:
            print(ep) 
            if ".jpg" not in entry.path:
                file_without_ext = os.path.splitext(ep)[0]
                jpg_file = "{}.jpg".format(file_without_ext)
                if os.path.exists(jpg_file):
                    continue
                bn = ntpath.basename(file_without_ext)
                #print("checking {}".format(bn)) 
                match =  re.match(r'^([A-Z0-9]+-[A-Z]*\d+)\D*', bn)
                if match == None:
                    print("{} cannot pass the reg exp, skip".format(bn))
                    continue
                product_id = ""
                for gg in match.groups():
                    product_id = gg
                    #print("Check {}".format(product_id))
                to_path = '{}/{}.jpg'.format(path, product_id)
                if (os.path.exists(to_path)):
                    continue
                hyper_link_path = 'http://www.javlibrary.com/ja/vl_searchbyid.php?keyword={}'.format(product_id)
               
                content = get_content(hyper_link_path)
                link_path = get_javlib_link(content, product_id)
                if link_path == None:
                    another_hyper_link_path = 'https://www.javbus.com/{}'.format(product_id)
                    another_content = get_content(another_hyper_link_path)
                    link_path = get_javbus_link(another_content, product_id)
                    if link_path == None:
                        continue
                to_path1 = '/Volumes/apen/0024Amazon/0024Amazon/cover/{}.jpg'.format(product_id)
                print("Download '{}' -> '{}".format(link_path, to_path1))
                dl.download_url(link_path, to_path1)

def scan(path):
    print("Try to scan folder: {}".format(path))
    try:
        entries = scan_jpg(path)
    except Exception:
        pass
    for entry in entries:
        print(entry.path)
        #move_single_file(entry.path, to_path)

if len(sys.argv) < 2:
    print("Usage: auto_dl_pic folder")
    sys.exit()

scan(os.path.expanduser(sys.argv[1]))
