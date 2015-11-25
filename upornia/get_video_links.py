from bs4 import BeautifulSoup
import urllib2
import download as dl
import codecs
import re
import glob, os
def get_video_links_from_model_page(av_str):
    from_path = "http://upornia.com/models/" + av_str + "/"
    to_path = "model/" + av_str
    dl.download_url(from_path, to_path)
    f = codecs.open(str(to_path), "r", "utf-8")
    if (f == None):
        return
#print("processing file: " + str(av_str))
    content = f.read()
    soup = BeautifulSoup(content);
    video_list_section = soup.find('div', {"id": "list_videos2_common_videos_list"})
    if video_list_section == None:
#print("video_list_section is empty")
        f.close()
        return
    items = video_list_section.find_all('article', {"class": "item"})
    if items == None:
#print("items are empty")
        f.close()
        return
    for item in items:
        url = item.find('a')
        if url == None:
#print("url is empty")
            continue;
        link = url['href']
        video_id = item['data-video-id']
#        print(link)
        dl_link_path = "video_url/" + video_id
        dl.download_url(link, dl_link_path)

    f.close()

