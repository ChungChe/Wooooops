#!/usr/bin/env python3


import os
#import urllib.request
import climber
from bs4 import BeautifulSoup
import download as dl


def get_ep_num(soup):
    li_sec = soup.find('div', {'id': 'list_tap'})
    all_ep = li_sec.findAll('li', {'class': 'ep'})
    return len(all_ep)

def get_iframe_video_link(soup):
    ifrmae_link_sec = soup.find('iframe')
    if ifrmae_link_sec == None:
        return
    return ifrmae_link_sec['src']
def get_video_page_source_link(soup):
    link_sec = soup.find('source')
    if link_sec == None:
        return
    return link_sec['src']

def get_final_video_link(link):
    content = climber.get_content(link)
    if content == None:
        return
    soup = BeautifulSoup(content)
    if soup == None:
        return
    
    iframe_vlink = "http://www.porn609.com/{}".format(get_iframe_video_link(soup))
    video_page = climber.get_content(iframe_vlink)
    if video_page == None:
        return
    soup2 = BeautifulSoup(video_page)
    if soup2 == None:
        return
    final_video_link = get_video_page_source_link(soup2) 
    return final_video_link 


def dl_videos(link):
    content = climber.get_content(link)
    if content == None:
        return
    soup = BeautifulSoup(content)
    boxes = soup.findAll('div', {'class': 'boxim'})
    if boxes == None:
        return

    links = []
    product_ids = []
    for sec in boxes:
        a_link_sec = sec.find('a')
        if a_link_sec == None:
            continue
        a_link = a_link_sec['href']
        a_title = a_link_sec['title']
        product_id = a_title.split(' ')[3]
        print("[{}] {}".format(product_id, a_link))
        links.append(a_link)
        product_ids.append(product_id)
    for idx, each_link in enumerate(links):
        content1 = climber.get_content(each_link)
        if content1 == None:
            continue
        soup1 = BeautifulSoup(content1)
        ep_num = get_ep_num(soup1)

        vid_link = get_final_video_link(each_link)
        if vid_link == '' or vid_link == None:
            continue
        # download this vid_link to product_id_1.mp4
        first_file_path = "{}_1.mp4".format(product_ids[idx])
        print("Download {} ...".format(first_file_path))
        if os.path.exists(first_file_path):
            print("{} exists, skip".format(first_file_path))
        else:
            dl.download_url(vid_link, first_file_path)

        #print(vid_link) 
        for i in range(2, ep_num + 1):
            new_link = "{}?ep={}".format(each_link, i)
            vid_link1 = get_final_video_link(new_link)
            if vid_link1 == '' or vid_link1 == None:
                continue
            #print(vid_link1)
            to_path = "{}_{}.mp4".format(product_ids[idx], i)
            print("Download {} ...".format(to_path))
            if os.path.exists(to_path):
                print("{} exists, skip".format(to_path))
            else:
                dl.download_url(vid_link1, to_path)

#dl_videos('http://www.porn609.com/?s=Hoshino+Asuka')
#dl_videos('http://www.porn609.com/?s=Katsuki+Yuuri')
#dl_videos('http://www.porn609.com/?s=Suzuki+Kiara')
dl_videos('http://www.porn609.com/?s=Kiyomi+Rei')
dl_videos('http://www.porn609.com/?s=Shirase+Erina')
dl_videos('http://www.porn609.com/?s=Kimino+Ayumi')
dl_videos('http://www.porn609.com/?s=Morikawa+Mau')
dl_videos('http://www.porn609.com/?s=Ayase+Meru')
