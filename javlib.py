#! /usr/bin/env python
# -*- coding: utf-8 -*-
# JAVLibrary hunter gather info to DB

import sqlite3 as db
import os
import climber2
#import re
from bs4 import BeautifulSoup
#from file_utility import file_holder

class javlib_hunter:
    # if db_file_name exists, connect it, otherwise, create it
    def __init__(self, db_file_name):
        self.__db_name = db_file_name
        self.__con = db.connect(self.__db_name)
        #self.__con.execute("PRAGMA journal_mode=WAL")
        self.__cur = self.__con.cursor()
        self.create_table_if_not_exists()
        self.__write_db = True 
#        self.__file_holder = file_holder()
    def __exit__(self):
        if self.__cur:
            self.__cur.close()
        if self.__con:
            self.__con.close()
    def get_match_pids(self, search_str):
        command = 'select pid, title, release_date from vid_table where title LIKE "%{}%"'.format(search_str, search_str)
        try:
            self.__cur.execute(command) 
            return self.__cur.fetchall()
        except Exception as e:
            print("Exception in get match pids {}, {}".format(search_str, e))
    def get_all_nid(self):
        try:
            self.__cur.execute('select nid from nid_table')
            return self.__cur.fetchall()
        except Exception as e:
            print("Exception in query nid, {}".format(e))
    def insert_nid_info(self, packed_data):
        if self.__write_db == False:
            return
        try:
            q = "(name, nid)"
            self.__cur.execute('insert or ignore into nid_table {} values (?,?)'.format(q), packed_data)
            self.__con.commit()
        except Exception as e:
            print("Exception in insert, {}".format(e))
            if self.__con:
                self.__con.rollback()
    def insert_vid_info(self, packed_data):
        if self.__write_db == False:
            return
        try:
            q = "(pid, title, release_date)"
            self.__cur.execute('insert or ignore into vid_table {} values (?,?,?)'.format(q), packed_data)
            self.__con.commit()
        except Exception as e:
            print("Exception in insert, {}".format(e))
            if self.__con:
                self.__con.rollback()

    def create_table_if_not_exists(self):
        try:
            # actress, preview_link and rapid_link may have a list, separate by a space char
            self.__cur.execute("create table if not exists nid_table (\
                name TEXT NOT NULL PRIMARY KEY, \
                nid TEXT \
            )")

            self.__cur.execute("create table if not exists vid_table (\
                pid TEXT NOT NULL, \
                title TEXT, \
                release_date TEXT, \
                PRIMARY KEY(pid, title) \
            )")
            self.__con.commit()
        except Exception as e:
            print("Exception in create_table {}".format(e))
            if self.__con:
                self.__con.rollback()

    def get_max_page_num(self, soup):
        href_data_sec = soup.find('a', {'class': 'page last'})
        if href_data_sec == None:
            return
        return int(href_data_sec['href'].split('page=')[1].split("\"")[0])
    def scan_vid_info(self, page_link):
        print(" #####  Parsing link {} ####".format(page_link))
        tmp_content = climber2.get_content(page_link)
        if tmp_content == None:
            print("QQ")
            return
        tmp_soup = BeautifulSoup(tmp_content, "html.parser")
        if tmp_soup == None:
            print("GG")
            return
        t = tmp_soup.find('table', {'class': 'videotextlist'})
        if t == None:
            print("TT")
            return
        match = t.findAll('tr')
        for m in match:
            if m.has_attr('class'):
                class_name = m['class']
                if class_name != None and len(class_name) > 0 and class_name[0] == 'header':
                    continue
            title = m.findAll('a')[3]['title']
            pid = title.split(' ')[0]
            release_date = m.findAll('td')[1].contents[0]
            print("{} {} {}".format(pid, title, release_date)) 
            packed_data = [pid, title, release_date]
            self.insert_vid_info(packed_data)
    def scan_str(self, scan_str):
        link = "http://www.javlibrary.com/tw/{}.php?list&mode=2&".format(scan_str)
        content = climber2.get_content(link)
        if content == None:
            return
        soup = BeautifulSoup(content, "html.parser")
        if soup == None:
            return
        max_page_num = self.get_max_page_num(soup)
        
        print("Max page num = {}".format(max_page_num))
        if max_page_num == None: # no extra page
            self.scan_vid_info(link)
        else: 
            for page_num in range(1, max_page_num + 1):
                page_link = "{}&page={}".format(link, page_num) 
                self.scan_vid_info(page_link)
    def scan_vid_by_nid(self, nid):
        link = "http://www.javlibrary.com/tw/vl_star.php?list&mode=2&s={}".format(nid)
        content = climber2.get_content(link)
        if content == None:
            return
        soup = BeautifulSoup(content, "html.parser")
        if soup == None:
            return
        max_page_num = self.get_max_page_num(soup)
        
        print("Max page num = {}".format(max_page_num))
        if max_page_num == None: # no extra page
            self.scan_vid_info(link)
        else: 
            for page_num in range(1, max_page_num + 1):
                page_link = "{}&page={}".format(link, page_num) 
                self.scan_vid_info(page_link)
        
    def scan_all_nid_videos(self):
        nids = self.get_all_nid() 
        for nid in nids:
            self.scan_vid_by_nid(nid[0])

    def scan_nid_info(self, page_link):
        print(" #####  Parsing link {} ####".format(page_link))
        tmp_content = climber2.get_content(page_link)
        if tmp_content == None:
            return
        tmp_soup = BeautifulSoup(tmp_content, "html.parser")
        if tmp_soup == None:
            return
        posts = tmp_soup.findAll('div', {'class': 'searchitem'})
        if posts == None:
            return
        for post in posts:
            nid = post['id'] 
            actress = post.find('a').contents[0]
            print("{} -> {}".format(actress, nid)) 
            packed_data = [actress, nid]
            self.insert_nid_info(packed_data)

    # www.javlibrary.com/tw/star_list.php?prefix=A to Z
    def scan_all_star(self):
        for l in range(ord('A'), ord('Z')):
            print(chr(l))
            link = 'http://www.javlibrary.com/tw/star_list.php?prefix={}'.format(chr(l))
            content = climber2.get_content(link)
            if content == None:
                return
            soup = BeautifulSoup(content, "html.parser")
            if soup == None:
                return
            max_page_num = self.get_max_page_num(soup)
            print("Max page num = {}".format(max_page_num))
            if max_page_num == None: # no extra page
                self.scan_nid_info(link)
            else: 
                for page_num in range(1, max_page_num + 1):
                    page_link = "{}&page={}".format(link, page_num) 
                    self.scan_nid_info(page_link)

if __name__ == "__main__":
    u = javlib_hunter("javlib70218.db")
    #u.update_rapid_link()
    #u.update_post_date()
    #u.scan_all_star()
    #u.scan_vid_by_nid('oy6a')
    #u.scan_all_nid_videos()
    u.scan_str("vl_newrelease")
    #u.scan_str("vl_update")
