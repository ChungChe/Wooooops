#!/usr/bin/env python3
import os
import climber
from bs4 import BeautifulSoup

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

    for page_num in range(1, max_page_num + 1):
        page_link = "http://www.javlibrary.com/tw/userposts.php?mode=&u=javmember&page={}".format(page_num) 
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
        
            print('<img src="{}"><br>'.format(img_link))
            ''' find title '''
            strong_sec = comment.find('strong')
            if strong_sec == None:
                continue
            title = strong_sec.find('a').contents[0]
            #print("Title: {}".format(title))
            text_sec = comment.find('textarea', {'class': 'hidden'})
            if text_sec == None:
                continue
            rapidgator_link = text_sec.contents[0].split('][')[0].split('url=')[1]
            #print(rapidgator_link)  
            print('<a href="{}">{}/</a><br><br>'.format(rapidgator_link, title))
print('<html><body>')
scan('http://www.javlibrary.com/tw/userposts.php?mode=&u=javmember')
print('</body></html>')
