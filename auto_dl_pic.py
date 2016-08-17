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
def scan_jpg(path):
    if not os.path.exists(path):
        print('Path not exists: {}'.format(path))
        return
    for entry in scandir.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scan_jpg(entry.path)  # see below for Python 2.x
        else:
            #print(entry.path) 
            if ".jpg" not in entry.path:
                file_without_ext = os.path.splitext(entry.path)[0]
                jpg_file = "{}.jpg".format(file_without_ext)
                if not os.path.exists(jpg_file):
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
                    
                    #print("{} doesn't exist, downloading...".format(product_id))
                    hyper_link_path = 'https://www.javbus.com/{}'.format(product_id)
                    content = ""
                    try:
                        content = u''.join(urllib.request.urlopen(hyper_link_path).read().decode('utf-8'))
                    #except urllib.error.HTTPError as e:
                    except Exception:
                        pass

                    soup = BeautifulSoup(content)
                    link = soup.find('a', {'class': 'bigImage'})
                    if link == None:
                        print('Cannot find jpg link from "{}", abort...'.format(product_id))
                        debug = soup.find('div', {'class': 'bol-md-9'})
                        if debug == None:
                            continue
                        print(debug)
                        continue
                    link_path = link['href']
                    to_path = '/Volumes/wd2/new_cover/{}.jpg'.format(product_id) 
                    if (os.path.exists(to_path)):
                        continue
                    print("Download '{}' -> '{}".format(link_path, to_path))
                    dl.download_url(link_path, to_path)

def scan(path):
    print("Try to scan folder: {}".format(path))
    entries = scan_jpg(path)

    for entry in entries:
        print(entry.path)
        #move_single_file(entry.path, to_path)

if len(sys.argv) < 2:
    print("Usage: auto_dl_pic folder")
    sys.exit()

scan(os.path.expanduser(sys.argv[1]))
