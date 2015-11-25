from bs4 import BeautifulSoup
import sys
import urllib2
import codecs
import re
import glob, os
os.chdir("video_url")
for file in glob.glob("*"):
    f = codecs.open(str(file), "r", "utf-8")
    if f == None:
        conitnue
    content = f.read()
    
    soup = BeautifulSoup(content);
    link_section = soup.find('div', {"class": "player-holder"})
    if link_section == None:
        f.close()
        continue
    script_section = link_section.find('script', text=re.compile(u'video_url'))
    if script_section == None:
        f.close()
        continue
    matches = re.findall(r'video_url: \'\S+\'', script_section.string)
    if len(matches) == 1:
        video_url1 = matches[0][12:]
        video_url = video_url1[:-1]
        print(video_url)
    f.close()
