#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
import re

def find_duplicate(input_file_name):
    f = codecs.open(input_file_name, "r", "utf-8")
    if f == None:
        return
    lines = f.readlines()
    d = dict()
    for line in lines:
        tok_list = re.split(" ", line)
        md5 = tok_list[0]
        mov_file_name = (' '.join(tok_list[1:]))
        if md5 in d:
            print mov_file_name.encode('utf-8') + ' conflicts with: ' + d[md5].encode('utf-8')
        else:
#print md5.encode('utf-8') + ' ' + mov_file_name.encode('utf-8')
            d[md5] = mov_file_name
#print "md5: " + md5 + ", file: " + mov_file_name.encode('utf-8')

find_duplicate('/home/pi/filelist_amazon')
