#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
#import sys

con = lite.connect('r94943159@ntu.edu.tw.db')

with con:    
    cur = con.cursor()    
    cur.execute("SELECT kind, md5, name FROM nodes")
    rows = cur.fetchall()
    for row in rows:
        if row[0] != "FILE":
            continue
        if row[1] == None:
            continue
        print str(row[1]) + ' ' + row[2].encode('utf-8')
