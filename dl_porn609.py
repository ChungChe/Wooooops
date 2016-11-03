#!/usr/bin/env python3


import os
import urllib.request
from bs4 import BeautifulSoup
import download as dl

def get_content(link):
    content = ""
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    try:
        req = urllib.request.Request(link, headers=hdr)
        with urllib.request.urlopen(req) as response:
            content = u''.join(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print("URLError Exception for {}, {}".format(link, e.reason))
        return
    except urllib.error.HTTPError as e:
        print("HTTPError Exception for {}, {}".format(link), e.reason)
        return
    except Exception:
        print("Exception for {}".format(link))
        return
    return content

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
    content = get_content(link)
    if content == None:
        return
    soup = BeautifulSoup(content)
    if soup == None:
        return
    
    iframe_vlink = "http://www.porn609.com/{}".format(get_iframe_video_link(soup))
    video_page = get_content(iframe_vlink)
    if video_page == None:
        return
    soup2 = BeautifulSoup(video_page)
    if soup2 == None:
        return
    final_video_link = get_video_page_source_link(soup2) 
    return final_video_link 


def dl_videos(link):
    content = get_content(link)
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
        content1 = get_content(each_link)
        if content1 == None:
            continue
        soup1 = BeautifulSoup(content1)
        ep_num = get_ep_num(soup1)

        vid_link = get_final_video_link(each_link)
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
            #print(vid_link1)
            to_path = "{}_{}.mp4".format(product_ids[idx], i)
            print("Download {} ...".format(to_path))
            if os.path.exists(to_path):
                print("{} exists, skip".format(to_path))
            else:
                dl.download_url(vid_link1, to_path)

dl_videos('http://www.porn609.com/?s=Hoshino+Asuka')
