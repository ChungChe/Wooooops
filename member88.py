#!/usr/bin/env python
# member88 extractor
import os
import climber2 as climber
from bs4 import BeautifulSoup
from rapid_identifier import rapidQQ 
from jinja2 import Environment
from file_utility import file_holder

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

def get_max_page_num(soup):
    href_data_sec = soup.find('a', {'class': 'page last'})
    if href_data_sec == None:
        return
    return int(href_data_sec['href'].split('page=')[1])

def scan(link):
    content = climber.get_content(link)
    if content == None:
        return
    soup = BeautifulSoup(content)
    if soup == None:
        return
    max_page_num = get_max_page_num(soup)
    tup_list = []
    qq = rapidQQ()
    f = file_holder()
    chunk_count = 0
    chunk_size = 120
    for page_num in range(1, max_page_num + 1):
        page_link = "http://www.javlibrary.com/tw/userposts.php?mode=&u=member88&page={}".format(page_num) 
        tmp_content = climber.get_content(page_link)
        if tmp_content == None:
            continue
        tmp_soup = BeautifulSoup(tmp_content)
        if tmp_soup == None:
            continue
        
        video_comments = tmp_soup.findAll('table', {'class': 'comment'})
        if video_comments == None:
            continue
        for comment in video_comments:
            first_img_link = comment.find('img', {'style': 'float:left'})
            if first_img_link == None:
                continue
            img_link = first_img_link['src']
        
            #print('<img src="{}"><br>'.format(img_link))
            ''' find title '''
            strong_sec = comment.find('strong')
            if strong_sec == None:
                continue
            title = strong_sec.find('a').contents[0]
            print('title: {}'.format(title))
            pid = title.split(' ')[0]
            if f.is_file_exists(pid) == True:
                print('pid {} exists, skip...'.format(pid))
                continue
            text_sec = comment.find('textarea', {'class': 'hidden'})
            if text_sec == None:
                continue

            rapidgator_link = text_sec.contents[0].split('][color=')[0].split('url=')[1]
            content = text_sec.contents[0].replace('[',' ').replace(']',' ').replace('\n',' ')
            tokens = content.split(' ')
            rapid_links = []
            for t in tokens:
                if 'url=http://rapidgator.net/file' in t:
                    rapid_link = t.replace('url=', '')
                    if qq.is_link_valid(rapid_link) == False:
                        continue
                    rapid_links.append(t.replace('url=', ''))
            if len(rapid_links) == 0:
                continue
            tup_list.append((title, img_link, rapid_links, pid))
            chunk_count += 1
            # write file for every 200 items
            if chunk_count > 0 and (chunk_count % chunk_size) == 0:
                tup_list.sort()
                output = Environment().from_string(HTML).render(tup_list=tup_list)
                file_name = "member88_output_{}.html".format(chunk_count / chunk_size)
                with open(file_name, 'w') as fp:
                    print("Write to file '{}'".format(file_name))
                    fp.write(output)
                    tup_list = []

if __name__ == "__main__":
    scan('http://www.javlibrary.com/tw/userposts.php?mode=&u=member88')
