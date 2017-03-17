#!/usr/bin/env python
# rapid link extractor
import os
import climber2 as climber
from bs4 import BeautifulSoup
#from rapid_identifier import rapidQQ 
from jinja2 import Environment
from file_utility import file_holder
import var
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
                    <h5><a href="{{ link }}">{{ link.replace('http://rapidgator.net/file/','') }}</a></h5>
                    {% endfor %}
                    </div>
                </div>
            </div>
        {% endfor %}
        </div>
    </body>
    </html>
"""
class javlib_member:
    def __init__(self, member_name):
        self.__str = member_name
        self.__f = file_holder()
        self.scan('{}{}'.format(var.javlib_path, self.__str))
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
    def scan(self, link):
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
            page_link = "{}{}&page={}".format(var.javlib_path, self.__str, page_num) 
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
                if self.__str == "member88":
                    tup = self.parse_member88(comment)
                elif self.__str == "maria01":
                    tup = self.parse_maria01(comment)
                elif self.__str == "javlustful":
                    tup = self.parse_javlustful(comment)
                elif self.__str == "uploader":
                    tup = self.parse_javlustful(comment)
                elif self.__str == "javmember":
                    tup = self.parse_member88(comment)
                if tup == None:
                    continue
                print(tup)
                tup_list.append(tup)
                chunk_count += 1
                if chunk_count > 0 and (chunk_count % chunk_size) == 0:
                    tup_list.sort()
                    output = Environment().from_string(HTML).render(tup_list=tup_list)
                    file_name = "web/static/html/{}_{}.html".format(self.__str, chunk_count / chunk_size)
                    with open(file_name, 'w') as fp:
                        print("Write to file '{}'".format(file_name))
                        fp.write(output)
                        tup_list = []
        # final
        if len(tup_list) > 0:
            tup_list.sort()
            output = Environment().from_string(HTML).render(tup_list=tup_list)
            file_name = "web/static/html/{}_{}.html".format(self.__str, chunk_count / chunk_size + 1)
            with open(file_name, 'w') as fp:
                print("Write to file '{}'".format(file_name))
                fp.write(output)
                tup_list = []

if __name__ == "__main__":
    javlib_member('javmember')
    javlib_member('uploader')
    javlib_member('javlustful')
    javlib_member('maria01')
    javlib_member('member88')
