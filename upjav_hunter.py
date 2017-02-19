#! /usr/bin/env python
# -*- coding: utf-8 -*-
# upjav hunter gather info to DB
import sqlite3 as db
import os
import climber2
import re
from bs4 import BeautifulSoup
from rapid_identifier import rapidQQ
from file_utility import file_holder
import var

class upjav_hunter:
    # if db_file_name exists, connect it, otherwise, create it
    def __init__(self, db_file_name):
        self.__db_name = db_file_name
        self.__con = db.connect(self.__db_name)
        self.__con.execute("PRAGMA journal_mode=WAL")
        self.__cur = self.__con.cursor()
        #if not os.path.exists(db_file_name):
        self.create_table_if_not_exists()
        # rapidQQ no login, just check if the link is valid
        self.__rapid = rapidQQ()
        self.__write_db = True 
        self.__file_holder = file_holder()
    def __exit__(self):
        if self.__cur:
            self.__cur.close()
        if self.__con:
            self.__con.close()
    def is_file_exists(self, search_str):
        return self.__file_holder.is_file_exists(search_str)

    def query_data(self, condition):
        fields = "post_date, pid, title, actress, cover_link, preview_link, rapid_link, available"
        #c = "available is 0 and is_censored is 1 and length(rapid_link) > 0"
        command = 'select {} from upjav_table where {}'.format(fields, condition)
        print("Query data commamd: {}".format(command))
        self.__cur.execute(command)
        match = self.__cur.fetchall()
        #print("Match: '{}'".format(match))
        if match == None or match == []:
            return
        if len(match) == 0:
            return
        
        match.sort(reverse=True)

        names = ['post_date', 'pid', 'title', 'actress', 'cover_link', 'preview_link' 'rapid_link']
        dict_list = []
        for e in match:
            is_avial = False
            if e[1] != None and e[6] != None:
                is_pid_avial = self.is_file_exists(e[1])
                rapid_file_name = e[6].split('/')[-1].split(".")[0]
                is_file_avail = self.is_file_exists(rapid_file_name)
                is_avial = is_pid_avial | is_file_avail
            dict_list.append({'post_date': e[0], 'pid': e[1], 'title': e[2], 'actress': e[3], 'cover_link': e[4], 'preview_link': e[5], 'rapid_link': e[6], 'available': is_avial})
        return dict_list 
    def query(self, condition, output_file = "debug_output"):
        #            0        1        2         3           4             5
        fields = "post_date, title, actress, cover_link, preview_link, rapid_link"
        #c = "available is 0 and is_censored is 1 and length(rapid_link) > 0"
        command = 'select {} from upjav_table where {}'.format(fields, condition)
        print(command)
        self.__cur.execute(command)
        match = self.__cur.fetchall()
        if match == None:
            return
        if len(match) == 0:
            return
        match.sort(reverse=True)
        print("{} records found".format(len(match)))
        with open("{}.html".format(output_file), 'w') as f:
            f.write("<html><body>\n")
            for m in match:
                f.write("{}<br>\n".format(m[1]))
                f.write('<img src="{}"></img><br>\n'.format(m[3]))
                for p in m[4].split(): 
                    if p == ' ' or len(p) < 2 or p is None:
                        continue
                    f.write('<img src="{}"></img><br>\n'.format(p))
                for r in m[5].split():
                    if r == ' ' or len(r) < 2 or r is None:
                        continue
                    f.write('<a href="{}">{}</a><br>\n'.format(r, r))
                f.write('<br>\n')
            f.write("</body></html>\n")
    def update_post_date(self):
        if self.__write_db == False:
            return
        self.__cur.execute('select url_id, post_date from upjav_table')
        match = self.__cur.fetchall()
        for m in match:
            new_date = m[1].replace(".", "-")
            try:
                self.__cur.execute('update upjav_table set post_date=:POSTDATE where url_id=:URLID', {"POSTDATE": new_date, "URLID": m[0]})
            except Exception as e:
                print("Exception in update_post_date {} {}".format(url_id, e))
                if self.__con:
                    self.__con.rollback()
        self.__con.commit()
    def update_rapid_link(self):
        if self.__write_db == False:
            return
        self.__cur.execute('select url_id, rapid_link from upjav_table where rapid_link is not null')
        match = self.__cur.fetchall()
        for m in match:
            l = m[1].split(' ')
            for item in l:
                if item == ' ' or len(item) == 0:
                    continue
                url = self.__rapid.is_link_valid(item)
                #set field rapid_link to NULL if the path is invalid
                if url == None:
                    print('{} is invalid, clear'.format(item))
                    try:
                        self.__cur.execute('update upjav_table set rapid_link=null where url_id=:URLID', {"URLID": m[0]})
                    except Exception as e:
                        print("Exception in set rapid_link {} to null {}".format(url, e))
                        if self.__con:
                            self.__con.rollback()
    def insert(self, packed_data):
        if self.__write_db == False:
            return
        try:
            q = "(url_id, post_date, title, actress, cover_link, preview_link, pid, release_date, is_censored, rapid_link, available, datetime, files)"
            self.__cur.execute('insert or ignore into upjav_table {} values (?,?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP,?)'.format(q), packed_data)
            self.__con.commit()
        except Exception as e:
            print("Exception in insert, {}".format(e))
            if self.__con:
                self.__con.rollback()
    def is_url_id_exists(self, url_id):
        try:
            self.__cur.execute('select url_id from upjav_table where url_id=:URLID', {"URLID": url_id})
            res = self.__cur.fetchone()
            if res != None:
                return True
        except Exception as e:
            print("Exception when find url_id '{}' in table".format(url_id))
        return False
    def create_table_if_not_exists(self):
        try:
            # actress, preview_link and rapid_link may have a list, separate by a space char
            self.__cur.execute("create table if not exists upjav_table (\
                url_id TEXT NOT NULL PRIMARY KEY, \
                post_date TEXT, \
                title TEXT, \
                actress TEXT, \
                cover_link TEXT, \
                preview_link TEXT, \
                pid TEXT, \
                release_date TEXT, \
                is_censored INTEGER, \
                rapid_link TEXT, \
                available INTEGER, \
                datetime DATETIME, \
                files TEXT \
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
    def get_post_info(self, soup):
        return soup.find('div', {'class': 'post_info'})
    def get_post_date(self, soup):
        pdate = soup.find('span', {'class': 'p_date'})
        return pdate.contents[0]
    def is_censored(self, soup):
        jav_cat_sec = soup.find('a', {'rel': 'category tag'})
        if jav_cat_sec != None:
            jav_cat = jav_cat_sec.contents[0]
            if jav_cat == "JAV Uncensored":
                return False
            elif jav_cat == "JAV IDOL":
                return True
            elif jav_cat == "JAV Censored":
                return True
        return None

    def get_rapid_links(self, soup):
        match_list = soup(text=re.compile(var.rapid_path))
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
        try:
            title = title_sec.contents[0]
            # remove [FHD], [HD] 
            title = title.replace("[FHD]", "")
            title = title.replace("[HD]", "")
            title_link = title_sec['href']
            if title_link == None:
                return None, None 
            return title, title_link
        except Exception as e:
            print("Exception parsing {}, {}".format(title_sec, e))
            return None, None
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
                actors = l[1:]
            elif len(l) == 1:
                ll = actress[0].split(':')
                if len(ll) > 1:
                    actors = ll[1:]
                else:
                    return None
        except Exception as e:
            print("Exception split {}, {}".format(actress[0], e))
        if actors != None:
            rm_lst = []
            for a in actors:
                if "—" in a:
                    rm_lst.append(a)
            for r in rm_lst:
                actors.remove(r)
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
        if re.match(r'^\[.*–.*\]', t.split()[0]) != None:
            return title.split()[0][1:-1].replace('–', '-')
        # Special handle
        # S-Cute xxx
        if "s-cute" in t:
            return title.split('#')[0][:-1]
        tok_2 = ['heyzo', 'real-diva', 'mywife-no', '1pondo', 'xxx-av', 
            'porno-eigakan', 'heydouga', 'gachinco', '1919gogo', 'c0930',
            'zipang', 'nyoshin', 'newhalfclub', 'caribbeancom', '10musume',
            'pacopacomama', 'asiatengoku', 'kin8tengoku', 'jukujo-club', 'roselip',
            'kt-joker', 'h0930', 'tokyo-hot', 'sm-miracle', 'blacked', 
            'hegre-a', 'x-art', 'lesshin', 'peepsamurai', 'av-sikou',
            'jgirl paradise', 'passion-hd', '15-daifuku'
        ]
        for e in tok_2:
            if e in t:
                tok = title.split(' ')
                return tok[0] + ' ' + tok[1]
        tok_1 = ['siro-', '200gana', 'mywife-', '259luxu-']
        for e in tok_1:
            if e in t:
                tok = title.split(' ')
                return tok[0]
        #"Hdddd kidddd... "
        if re.match(r'^h\d+ ki\d+', t) != None:
            tok = t.split(' ')
            return tok[0] + ' ' + tok[1]
        #"Hdddd oridddd... "
        if re.match(r'^h\d+ ori\d+', t) != None:
            tok = t.split(' ')
            return tok[0] + ' ' + tok[1]
        # Uncensored-XXX 
        if "uncensored-" in t:
            return title.split(' ')[0].split('Uncensored-')[1]
        tok_3 = ['tokyo hot', 'girlsdelta']
        for e in tok_3:
            if e in t:
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
        count = 0
        for page_num in range(1, max_page_num + 1):
            print(" ##################  Loading Page {} ##################".format(page_num))
            page_link = "{}/page/{}".format(var.upjav_path, page_num) 
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
                if title == None: 
                    continue
                url_id = title_link.split("http://upjav.org/")[1][:-1]
                if self.is_url_id_exists(url_id):
                    sticky = post.find('span', {'class': 'title_sticky'})
                    if sticky == None:
                        print("URL ID: {} exist, skip".format(url_id))
                        return
                    else:
                        continue

                pid = self.extract_pid(title)
                print("PID: {}".format(pid))
                cover_link = self.get_cover_link(post)
                print("Cover : {}".format(cover_link))
                print("URL ID: {}".format(url_id))
                inner_soup = self.get_inner_soup(title_link)
                if inner_soup == None:
                    continue
                actors = self.extract_actress(inner_soup)
                actor_str = ""
                if actors != None:
                    for actor in actors:
                        actor_str += actor + ' '
                    if actor_str != None:
                        print("Actor: {}".format(actor_str))

                date = self.extract_date(inner_soup)
                if date != None:
                    print("Release Date: {}".format(date))
                post_info = self.get_post_info(inner_soup)
                is_censored = self.is_censored(post_info)
                post_date = self.get_post_date(post_info)
                post_date = post_date.replace(".", "-")
                print("Post Date: {}".format(post_date))
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
                files = []
                for l in rapid_links:
                    # if the link is available
                    files.append(l.split('/')[-1].split('.')[0])
                    #if self.__rapid.is_link_valid(l) == None:
                    #    continue
                    rapid_str += l + ' '
                print("Rapid Str: {}".format(rapid_str))
                avail = 0
                if pid != None and len(pid) > 3 and '-' in pid:
                    path = '{}/{}/{}/{}'.format(var.acd_sorted_path, pid[0], pid.split('-')[0], pid)
                    if os.path.exists(path):
                        avail = 1
                
                for f in files:
                    if self.is_file_exists(f):
                        avail = 1
                        break

                packed_data = [url_id, post_date, title, actor_str, cover_link, preview_str, pid, date, censored, rapid_str, avail, ' '.join(files)]   
                self.insert(packed_data)
                count += 1

if __name__ == "__main__":
    u = upjav_hunter("upjav170218.db")
    #u.update_rapid_link()
    #u.update_post_date()
    u.scan_top_level(var.upjav_path)
