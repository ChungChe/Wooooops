#! /usr/bin/env python
# -*- coding: utf-8 -*-
# upjav hunter gather info to DB
import sqlite3 as db
import os
import climber2
import re
from bs4 import BeautifulSoup

class upjav_hunter:
    # if db_file_name exists, connect it, otherwise, create it
    def __init__(self, db_file_name):
        self.__db_name = db_file_name
        self.__con = db.connect(self.__db_name)
        self.__cur = self.__con.cursor()
        #if not os.path.exists(db_file_name):
        self.create_table_if_not_exists()
    def __exit__(self):
        if self.__cur:
            self.__cur.close()
        if self.__con:
            self.__con.close()
    def insert(self, packed_data):
        try:
            self.__cur.execute('insert or ignore into upjav_table (url_id, title, actress, cover_link, preview_link, pid, release_date, is_censored, rapid_link) values (?,?,?,?,?,?,?,?,?)', packed_data)
            self.__con.commit()
        except Exception as e:
            print("Exception in create_table {}".format(e))
            if self.__con:
                self.__con.rollback()
    def create_table_if_not_exists(self):
        try:
            # actress, preview_link and rapid_link may have a list, separate by a space char
            self.__cur.execute("create table if not exists upjav_table (\
                url_id TEXT NOT NULL PRIMARY KEY, \
                title TEXT, \
                actress TEXT, \
                cover_link TEXT, \
                preview_link TEXT, \
                pid TEXT, \
                release_date TEXT, \
                is_censored INTEGER, \
                rapid_link TEXT \
            )")
            self.__con.commit()
        except Exception as e:
            print("Exception in create_table {}".format(e))
            if self.__con:
                self.__con.rollback()

    def get_max_page_num(self, soup):
        href_data_sec = soup.find('a', {'class': 'last'})
        if href_data_sec == None:
            return
        return int(href_data_sec['href'].split('page/')[1].split("/")[0])

    def get_inner_soup(self, link):
        content = climber2.get_content(link)
        if content == None:
            return None
        return BeautifulSoup(content, "html.parser")
    def is_censored(self, soup):
        jav_cat_sec_all = soup.findAll('a', {'rel': 'category tag'})
        for jav_cat_sec in jav_cat_sec_all:
            jav_cat = jav_cat_sec.contents[0]
            if jav_cat == "JAV Uncensored":
                return False
            elif jav_cat == "JAV Censored":
                return True
        return None

    def get_rapid_links(self, soup):
        match_list = soup(text=re.compile('http://rapidgator.net/'))
        return match_list

    def get_preview_img_link(self, soup):
        entry_sec = soup.find('div', {'class': 'entry'})
        if entry_sec == None:
            return None
        #print(entry_sec)
        l = []
        match_list = entry_sec.findAll('a', {'href': re.compile('jpeg')})
        for m in match_list:
            l.append(m['href'])
        match_list1 = entry_sec.findAll('a', {'href': re.compile('jpg')})
        for m in match_list1:
            l.append(m['href'])
        return l
    def get_title_and_title_link(self, soup): 
        title_sec = soup.find('h2', {'class': 'title'}).find('a')
        if title_sec == None:
            return None, None
        title = title_sec.contents[0]
        title_link = title_sec['href']
        if title_link == None:
            return None, None 
        return title, title_link
    def extract_actress(self, soup):
        entry_sec = soup.find('div', {'class': 'entry'})
        if entry_sec == None:
            return None
        actress = []
        match1 = entry_sec(text=re.compile(ur'出演', re.UNICODE))
        if match1 != None:
            actress = match1
        if not actress:
            return None
        actors = None
        try:
            l = actress[0].split(' ')
            if len(l) > 1: 
                actors = l[1]
            elif len(l) == 1:
                ll = actress[0].split(':')
                if len(ll) > 1:
                    actors = ll[1]
                else:
                    return None
        except Exception as e:
            print("Exception split {}, {}".format(actress[0], e))
        if actors != None and "—" in actors:
            actors = None
        return actors
    def extract_date(self, soup):
        entry_sec = soup.find('div', {'class': 'entry'})
        if entry_sec == None:
            return None
        date = []
        match1 = entry_sec(text=re.compile(ur'発売日', re.UNICODE))
        match2 = entry_sec(text=re.compile(ur'公開日', re.UNICODE))
        match3 = entry_sec(text=re.compile(ur'販売日', re.UNICODE))
        match4 = entry_sec(text=re.compile(ur'配信日', re.UNICODE))

        if match1 != None:
            date = match1
        elif match2 ==None:
            date = match2
        elif match3 != None:
            date = match3
        elif match4 != None:
            date = match4
        if not date:
            return None
        release_date = None
        try:
            release_date = date[0].split(' ')[1]
        except Exception as e:
            print("Exception split {}, {}".format(date[0], e))
        return release_date
    def extract_pid(self, title):
        t = title.lower()
        # normal pid [AAA-3333]
        if re.match(r'^\[.*-.*\]', t.split()[0]) != None:
            return title.split()[0][1:-1]
        # Special handle
        # SIRO-xxxx
        if "siro-" in t:
            tok = title.split(' ')
            return tok[0]
        # 200GANA 
        if "200gana" in t:
            tok = title.split(' ')
            return tok[0]
        # S-Cute xxx
        if "s-cute" in t:
            return title.split('#')[0][:-1]
        # HEYZO
        if "heyzo" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # Real-diva 
        if "real-diva" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # Mywife-NO ..."
        if "mywife-no" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # 1pondo
        if "1pondo" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # XXX-AV 
        if "xxx-av" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # Porno-Eigakan 
        if "porno-eigakan" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # Heydouga 
        if "heydouga" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # Gachinco 
        if "gachinco" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # C0930 
        if "c0930" in  t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # zipang 
        if "zipang" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # Nyoshin 
        if "nyoshin" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # Newhalfclub 
        if "newhalfclub" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # caribbeancom 
        if "caribbeancom" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # 10musume 
        if "10musume" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # pacopacomama 
        if "pacopacomama" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # Asiatengoku 
        if "asiatengoku" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # Kin8tengoku 
        if "kin8tengoku" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # Jukujo-club
        if "jukujo-club" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # Roselip 
        if "roselip" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # Kt-joker 
        if "Kt-joker" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # H0930 
        if "h0930" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        #"Hdddd kidddd... "
        if re.match(r'^h\d+ ki\d+', t) != None:
            tok = t.split(' ')
            return tok[0] + ' ' + tok[1]
        #"Hdddd oridddd... "
        if re.match(r'^h\d+ ori\d+', t) != None:
            tok = t.split(' ')
            return tok[0] + ' ' + tok[1]
        # Tokyo-Hot 
        if "tokyo-hot" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # SM-miracle 
        if "sm-miracle" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # BLACKED 
        if "blacked" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # Hegre-Art 
        if "hegre-art" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # X-Art 
        if "x-art" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # Lesshin 
        if "lesshin" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1]
        # Uncensored-XXX 
        if "uncensored-" in t:
            return title.split(' ')[0].split('Uncensored-')[1]
        # tokyo hot 
        if "tokyo hot" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1] + ' ' + tok[2]
        # Real Street Angels xxxx 
        if "real street angels" in t:
            tok = title.split(' ')
            return tok[0] + ' ' + tok[1] + ' ' + tok[2] + ' ' + tok[3]
        print("Unknown pid for '{}'".format(title))
        return None
    def get_cover_link(self, soup):
        first_img_link = soup.find('img', {'border': '0'})
        if first_img_link == None:
            return None
        cover_link = first_img_link['src']
        return cover_link
    def scan_top_level(self, link):
        content = climber2.get_content(link)
        if content == None:
            return
        soup = BeautifulSoup(content, "html.parser")
        if soup == None:
            return
        max_page_num = self.get_max_page_num(soup)
        print("Max page num = {}".format(max_page_num))
        size_per_page = 40
        count = 0
        for page_num in range(1, max_page_num + 1):
            page_link = "http://upjav.org/page/{}".format(page_num) 
            tmp_content = climber2.get_content(page_link)
            if tmp_content == None:
                continue
            tmp_soup = BeautifulSoup(tmp_content, "html.parser")
            if tmp_soup == None:
                continue
            posts = tmp_soup.findAll('div', {'class': 'post'})
            if posts == None:
                continue
            for post in posts:
                print("====== section {} =====".format(count))
                title, title_link = self.get_title_and_title_link(post)
                print("Title: {}".format(title))
                print("Title Link: {}".format(title_link))
                
                pid = self.extract_pid(title)
                print("PID: {}".format(pid))
                cover_link = self.get_cover_link(post)
                print("Cover : {}".format(cover_link))
                url_id = title_link.split("http://upjav.org/")[1][:-1]
                print("URL ID: {}".format(url_id))
                inner_soup = self.get_inner_soup(title_link)
                if inner_soup == None:
                    continue
                actor = self.extract_actress(inner_soup)
                if actor != None:
                    print("Actor: {}".format(actor))

                date = self.extract_date(inner_soup)
                if date != None:
                    print("Release Date: {}".format(date))
                is_censored = self.is_censored(inner_soup)
                censored = 0
                if is_censored == True:
                    censored = 1
                print("Censored: {}".format(is_censored))
                preview_imgs = self.get_preview_img_link(inner_soup)
                preview_str = ""
                for p in preview_imgs:
                    preview_str += p + ' '
                
                print("Preview Imgs: {}".format(preview_str))

                rapid_links = self.get_rapid_links(inner_soup)
                rapid_str = ""
                for l in rapid_links:
                    rapid_str += l + ' '
                print("Rapid Str: {}".format(rapid_str))
                packed_data = [url_id, title, actor, cover_link, preview_str, pid, date, censored, rapid_str]   
                self.insert(packed_data)
                count += 1

if __name__ == "__main__":
    u = upjav_hunter("upjav.db")
    u.scan_top_level("http://upjav.org")
