from bs4 import BeautifulSoup
import urllib2
import download as dl
import codecs
import re
import glob, os
os.chdir("actress_page")
for file in glob.glob("*"): 
    f = codecs.open(str(file), "r", "utf-8")
    if f == None:
        conitnue
    print("processing file: " + str(file))
    content = f.read()

    soup = BeautifulSoup(content);
    waterfall = soup.find('div', {"id": "waterfall"})
    if waterfall == None:
        f.close()
        continue
    items = waterfall.find_all('a', {"class": "avatar-box"})
    if items == None:
        f.close()
        continue
    for item in items: 
        img_tag = item.find('img')
        if img_tag == None:
            f.close()
            continue
        name = img_tag['title']
        img_url = img_tag['src']
        print(name)
        url = item['href']
        dl.download_url(url, "../actress/" + name)
        if "nowprinting.gif" in img_url:
            print('No image, skip')
        else:
            dl.download_url(img_url, "../av_icon/" + name + ".jpg")
    os.rename(file, "../proceed_page/" + str(file))
    f.close()
