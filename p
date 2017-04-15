#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from peewee import *
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: {} search_string".format(sys.argv[0]))
        sys.exit()
    db = SqliteDatabase('link_ext.db')

    class item(Model):
        pid = CharField()
        title = CharField()
        img_link = CharField()
        rapid_links = CharField()
        class Meta:
            database = db
    s = sys.argv[1]
    m = item.select().where(item.pid.contains(s) | item.title.contains(s)).order_by(item.pid)
    for ele in m:
        print(ele.title)
        link_str = ele.rapid_links.replace('u','').replace("'","").replace(',', ' ').replace('[','').replace(']','')
        links = link_str.split()
        for l in links:
            print(l)
        print('')
    print("Total {} matches".format(len(m)))
