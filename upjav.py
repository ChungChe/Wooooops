# upjav extractor
# only extract title, image, and rapidgator links

#!/usr/bin/env python3
import os
import climber
import re
from bs4 import BeautifulSoup

def get_max_page_num(soup):
    href_data_sec = soup.find('a', {'class': 'last'})
    if href_data_sec == None:
        return
    return int(href_data_sec['href'].split('page/')[1].split("/")[0])

def get_inner_soup(link):
    content = climber.get_content(link)
    if content == None:
        return None
    return BeautifulSoup(content)

def get_rapid_links(link):
    soup = get_inner_soup(link)
    if soup == None:
        return
    match_list = soup(text=re.compile('http://rapidgator.net/'))
    return match_list

def get_preview_img_link(link):
    soup = get_inner_soup(link)
    if soup == None:
        return None
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
def create_html_page(i, buf):
    file_name = 'upjav_{}.html'.format(i)
    with open(file_name, 'w') as f:
        f.write('<html><body>\n{}</body></html>\n'.format(buf))
    
def scan_top_level(link):
    content = climber.get_content(link)
    if content == None:
        return
    soup = BeautifulSoup(content)
    if soup == None:
        return
    max_page_num = get_max_page_num(soup)
    print("Max page num = {}".format(max_page_num))
    size_per_page = 40
    count = 0
    buf = ""
    for page_num in range(1, max_page_num + 1):
        page_link = "http://upjav.org/page/{}".format(page_num) 
        tmp_content = climber.get_content(page_link)
        if tmp_content == None:
            continue
        tmp_soup = BeautifulSoup(tmp_content)
        if tmp_soup == None:
            continue
        
        posts = tmp_soup.findAll('div', {'class': 'post'})
        if posts == None:
            continue
        for post in posts:
            print("====== section {} =====".format(count))
            ''' find title '''
            title_sec = post.find('h2', {'class': 'title'}).find('a')
            if title_sec == None:
                continue
            #print("Title Sec: {}".format(title_sec))
            title = title_sec.contents[0]
            print("Title: {}".format(title))
            buf += "{}<br>\n".format(title) 
            ''' find img link '''
            first_img_link = post.find('img', {'border': '0'})
            if first_img_link == None:
                continue
            img_link = first_img_link['src']
            
            title_link = title_sec['href']
            print("Title Link: {}".format(title_link))
            if title_link == None:
                continue
            
            print("Image : {}".format(img_link)) 
            buf += '<a href="{}"><img src="{}"></img></a><br>\n'.format(title_link, img_link)
            
            preview_imgs = get_preview_img_link(title_link)
            for p in preview_imgs:
                buf += '<img src="{}"></img><br>\n'.format(p)
                print(p)
            
            rapid_links = get_rapid_links(title_link)
            for l in rapid_links:
                buf += '<a href="{}">{}</a><br>\n'.format(l, l)
                print(l)
            buf += '<br>\n'
            
            count += 1
            if count % size_per_page == 0:
                idx = count / 40
                print("flush to file_{}".format(idx))
                create_html_page(idx, buf)
                buf = ""

scan_top_level("http://upjav.org")
