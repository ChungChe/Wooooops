#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
import re
def find_diff(input_file_name, dic):
    f = codecs.open(input_file_name, "r", "utf-8")
    if f == None:
        return
    lines = f.readlines()
    for line in lines:
        tok_list = re.split(" ", line)
        md5 = tok_list[0]
        mov_file_name = (' '.join(tok_list[1:]))
        if md5 not in dic:
            print mov_file_name.encode('utf-8'),
            # hack
            dic[md5] = mov_file_name

def set_dic(input_file_name):
    f = codecs.open(input_file_name, "r", "utf-8")
    if f == None:
        return
    d = dict()
    lines = f.readlines()
    for line in lines:
        tok_list = re.split(" ", line)
        md5 = tok_list[0]
        mov_file_name = (' '.join(tok_list[1:]))
        if md5 not in d:
            d[md5] = mov_file_name
    return d

amazon_d = set_dic('/home/pi/filelist_amazon')
find_diff('/home/pi/hubic_md5_list', amazon_d)
