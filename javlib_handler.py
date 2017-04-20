#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from peewee import *
from file_utility import file_holder

# Use Deferring initialization
# https://peewee.readthedocs.io/en/2.0.2/peewee/cookbook.html
db = SqliteDatabase(None)
class item(Model):
    pid = CharField()
    title = CharField()
    img_link = CharField()
    rapid_links = CharField()
    class Meta:
        database = db

class javlib_handler():
    def __init__(self):
        db.init('link_ext.db')
        self.fh = file_holder()
    def search(self, s):
        m = item.select().where(item.pid.contains(s) | item.title.contains(s)).order_by(item.pid)
        new_m = []
        for ele in m:
            #print(ele.pid)
            if self.fh.is_file_exists(ele.pid):
                continue
            else:
                new_m.append(ele)
        return new_m
    def get_rapid_links(self, r):
        #print(r)
        link_str = r.replace('u','').replace("'","").replace(',', ' ').replace('[','').replace(']','')
        return link_str.split()

