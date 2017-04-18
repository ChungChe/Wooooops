#!/usr/bin/env python
# link extractor 
import os
import climber2 as climber
from bs4 import BeautifulSoup
#from rapid_identifier import rapidQQ 
from jinja2 import Environment
from file_utility import file_holder
import var
from peewee import *
# title, img_link, rapid_links, pid
HTML = """
    <html>
    <head> </head>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    <link rel="icon" href="data:;base64,=">
    </head>
    <title> </title>
    <body>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        <script src="/static/js/bootstrap.min.js"></script>
        <script src="/static/js/nav_handler.js"></script>
        <div class="row align-items-center">
        {% for data in tup_list %}
            {% if (loop.index - 1) > 0 and (loop.index  - 1) % 6 == 0 %}
                </div><div class="row align-items-center">
            {% endif %}
            <div class="col-md-2">
                <div class="thumbnail">
                    <h4 class="pull-center">{{ loop.index }}</h4>
                    <a target="_blank" href="https://www.javbus.com/{{ data[3] }}"><img src="{{ data[1] }}"</img></a>
                    <div class="caption">
                    <h4>{{ data[0] }}</h4>
                    {% for link in data[2] %}
                        <h5><a target="_blank" href="http://192.168.1.150:9487/dl?link={{ link }}">Download</a></h5>
                    {% endfor %}
                    </div>
                </div>
            </div>
        {% endfor %}
        </div>
    </body>
    </html>
"""

db = SqliteDatabase('link_ext.db')


class item(Model):
    pid = CharField()
    title = CharField()
    img_link = CharField()
    rapid_links = CharField()
    class Meta:
        database = db

class javlib_member:
    def __init__(self):
        self.__f = file_holder()
    def scan_all(self):
        ary = ['fireworks', 'javupdate', 'javmember', 'uploader', 'javlustful', 'maria01', 'member88']
        for e in ary:
            #scan_string = '{}{}'.format(var.javlib_path, e)
            self.scan(e)
    def get_max_page_num(self, soup):
        href_data_sec = soup.find('a', {'class': 'page last'})
        if href_data_sec == None:
            return
        return int(href_data_sec['href'].split('page=')[1])
    def parse_maria01(self, comment):
        
        ''' find title '''
        strong_sec = comment.find('strong')
        if strong_sec == None:
           return 
        title = strong_sec.find('a').contents[0]
        print('title: {}'.format(title))
        
        pid = title.split(' ')[0]
        #print('pid: {}'.format(pid))
        if self.__f.is_file_exists(pid) == True:
            print('pid {} exists, skip...'.format(pid))
            return
        
        first_img_link = comment.find('img', {'style': 'float:left'})
        if first_img_link == None:
           return 
        img_link = first_img_link['src']
        #print('img_link: {}'.format(img_link)) 
        
        table_content = comment.find('td', {'class': 't'})
        if table_content == None:
            return
        text_area = table_content.find('textarea', {'class': 'hidden'})
        if text_area == None:
            return
        content = text_area.contents[0].replace('[url]',' ').replace('[/url]',' ')
        tokens = content.split(' ')
        rapid_links = []
        for t in tokens:
            if 'http://rapidgator.net/file' in t:
                rapid_link = t.replace('url=', '')
                #if qq.is_link_valid(rapid_link) == False:
                #    continue
                rapid_links.append(rapid_link)
        if len(rapid_links) == 0:
            return None
        #print(rapid_links)
        return (title, img_link, rapid_links, pid)
    def parse_member88(self, comment):
    
        ''' find title '''
        strong_sec = comment.find('strong')
        if strong_sec == None:
           return 
        title = strong_sec.find('a').contents[0]
        print('title: {}'.format(title))
        pid = title.split(' ')[0]
        if self.__f.is_file_exists(pid) == True:
            print('pid {} exists, skip...'.format(pid))
            return
        
        first_img_link = comment.find('img', {'style': 'float:left'})
        if first_img_link == None:
           return 
        img_link = first_img_link['src']
        
        text_sec = comment.find('textarea', {'class': 'hidden'})
        if text_sec == None:
            return 
        print(text_sec.contents[0])
        #rapidgator_link = ""
        #if self.__str == "member88":
        #rapidgator_link = text_sec.contents[0].split('][color=')[0].split('url=')[1]
        #elif self.__str == "maria01":
        #    rapidgator_link = text_sec.contents[0].split('[url]')[1].split('[/url]')[0]
        #print(rapidgator_link)

        content = text_sec.contents[0].replace('[',' ').replace(']',' ').replace('\n',' ')
        tokens = content.split(' ')
        rapid_links = []
        for t in tokens:
            if 'url=http://rapidgator.net/file' in t:
                rapid_link = t.replace('url=', '')
                #if qq.is_link_valid(rapid_link) == False:
                #    continue
                rapid_links.append(t.replace('url=', ''))
        if len(rapid_links) == 0:
            #continue
            return
        return (title, img_link, rapid_links, pid)
    def parse_javlustful(self, comment):
    
        ''' find title '''
        strong_sec = comment.find('strong')
        if strong_sec == None:
           return 
        title = strong_sec.find('a').contents[0]
        print('title: {}'.format(title))
        pid = title.split(' ')[0]
        if self.__f.is_file_exists(pid) == True:
            print('pid {} exists, skip...'.format(pid))
            return
        
        first_img_link = comment.find('img', {'style': 'float:left'})
        if first_img_link == None:
           return 
        img_link = first_img_link['src']
        
        text_sec = comment.find('textarea', {'class': 'hidden'})
        if text_sec == None:
            return 
        content = text_sec.contents[0].replace('[url]',' ').replace('[/url]',' ').replace('\n',' ')
        tokens = content.split(' ')
        rapid_links = []
        for t in tokens:
            if 'http://rapidgator.net/file' in t:
                print(t)
                rapid_links.append(t)
        if len(rapid_links) == 0:
            return
        return (title, img_link, rapid_links, pid)
    def scan(self, uid):
        link = '{}{}'.format(var.javlib_path, uid)
        print("link = '{}'".format(link))
        content = climber.get_content(link)
        if content == None:
            return
        soup = BeautifulSoup(content, "html.parser")
        if soup == None:
            return
        max_page_num = self.get_max_page_num(soup)
        print("Max page: {}".format(max_page_num))
        tup_list = []
        #qq = rapidQQ()
        chunk_count = 0
        chunk_size = 240 
        for page_num in range(1, max_page_num + 1):
            page_link = "{}{}&page={}".format(var.javlib_path, uid, page_num) 
            tmp_content = climber.get_content(page_link)
            if tmp_content == None:
                continue
            tmp_soup = BeautifulSoup(tmp_content, "html.parser")
            if tmp_soup == None:
                continue
            
            video_comments = tmp_soup.findAll('table', {'class': 'comment'})
            if video_comments == None:
                continue
            for comment in video_comments:
                tup = None
                if uid == "member88":
                    tup = self.parse_member88(comment)
                elif uid == "maria01":
                    tup = self.parse_maria01(comment)
                elif uid == "javlustful":
                    tup = self.parse_javlustful(comment)
                elif uid == "uploader":
                    tup = self.parse_javlustful(comment)
                elif uid == "fireworks":
                    tup = self.parse_javlustful(comment)
                elif uid == "javmember":
                    tup = self.parse_member88(comment)
                elif uid == "javupdate":
                    tup = self.parse_maria01(comment)
                if tup == None:
                    continue
                #print(tup)
                try:
                    item.select().where((item.pid == tup[3]) & (item.title == tup[0]) & item.rapid_links == tup[2])
                except item.DoesNotExist:
                    item.create(pid=tup[3], title=tup[0], img_link=tup[1], rapid_links=tup[2])
                    print("Create new item for {}".format(tup[3]))
                #new_item, is_exist = item.get_or_create(pid=tup[3], title=tup[0], img_link=tup[1],rapid_links=tup[2])
                #try:
                #    item.select(item.pid, item.title, item.img_link, item.rapid_links).
                #where(item.pid == tup[3] & item.title == tup[0] & item.img_link == tup[1] & item.rapid_links == tup[2])[0]
                    #item.get(pid=tup[3], title=tup[0], img_link=tup[1], rapid_links=tup[2])
                #except IndexError:
                #item.create(pid=tup[3], title=tup[0], img_link=tup[1], rapid_links=tup[2])
                tup_list.append(tup)
                chunk_count += 1
                if chunk_count > 0 and (chunk_count % chunk_size) == 0:
                    tup_list.sort()
                    output = Environment().from_string(HTML).render(tup_list=tup_list)
                    file_name = "web/static/html/{}_{}.html".format(uid, chunk_count / chunk_size)
                    with open(file_name, 'w') as fp:
                        print("Write to file '{}'".format(file_name))
                        fp.write(output)
                        tup_list = []
        # final
        if len(tup_list) > 0:
            tup_list.sort()
            output = Environment().from_string(HTML).render(tup_list=tup_list)
            file_name = "web/static/html/{}_{}.html".format(uid, chunk_count / chunk_size + 1)
            with open(file_name, 'w') as fp:
                print("Write to file '{}'".format(file_name))
                fp.write(output)
                tup_list = []
    def gen_page(self):
        items = item.select().order_by(item.pid)
        tup_list = []
        for i in items:
            #print('pid = {}, title = {}'.format(i.pid, i.title))
            # handle rapid_links
            tmp = i.rapid_links.replace("[","").replace("]","").replace("u'", "").replace("'", "").replace(',', ' ')
            #print("tmp = {}".format(tmp))
            links = tmp.split()
            #print('rapid_links = {}'.format(links))
            tup = (i.title, i.img_link, links, i.pid)
            tup_list.append(tup)
            #return (title, img_link, rapid_links, pid)
        print("Tuplist len: {}".format(len(tup_list)))
        # list to chunks
        chunk_size = 240
        c = [tup_list[i:i + chunk_size] for i in xrange(0, len(tup_list), chunk_size)]
        print("Chunk num: {}".format(len(c)))
        for idx, ele in enumerate(c):
            output = Environment().from_string(HTML).render(tup_list=ele)
            file_name = "web/static/html/{}_{}.html".format("link_ext", idx)
            with open(file_name, 'w') as fp:
                print("Write to file '{}'".format(file_name))
                fp.write(output)

if __name__ == "__main__":

    try:
        item.create_table()
    except Exception as e:
        print("Error: {}".format(e))
    j = javlib_member()
    j.gen_page()
