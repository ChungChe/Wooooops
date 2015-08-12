# -*- coding: utf-8 -*- 
from bs4 import BeautifulSoup
import sqlite3 as db
import sys
import urllib2
import codecs
import re
import glob, os
import download as dl
import toSqlite as w
os.chdir("page");
def get_actressInfo(soup, av_ID):
    title = soup.find('meta', {"property": "og:title"})
    if title == None:
        print("Title is empty, skip")
        return None
    av_name = title['content']
    name_list = re.split('\(|\)', av_name)
    # 1. Name
    if name_list == None:
        print("Name is empty, skip")
        return None
    av_name = name_list[0]
    print(av_name)
#------ profile section is buggy, see profile 3384 --------
    profile = soup.find('dl', {"class": "profile"})
    if profile == None:
        print("Profile is empty, skip")
        return None
    ddSection = profile.find_all('dd')
    ddLen = len(ddSection)
    if ddLen == 8:
        base = 1;
    else:
        base = 0;
    # 2. Birthdate
    birthdate = None
    if len(ddSection[base].contents)  == 2:
        birthdate = ddSection[base].contents[1]
        birthdate = birthdate.replace(u"年","-")
        birthdate = birthdate.replace(u"月","-")
        birthdate = birthdate.replace(u"日","")
        print(birthdate)
    bloodType = None
    # 3. Blood type
    if len(ddSection[base+1].contents) == 2:
        bloodType = ddSection[base+1].contents[1]
        bloodType = bloodType.replace(u"型","")
        if bloodType == '-':
            bloodType = None
        print(bloodType)
    # 4. Birthplace
    birthplace = None 
    if len(ddSection[base+2].contents) == 2:
        birthplace = ddSection[base+2].contents[1]
        print(birthplace)
    # 5. Height
    height = None
    if len(ddSection[base+3].contents) == 2:
        height = ddSection[base+3].contents[1]
        height = height.replace("cm","")
        print(height)
    # 6. Measurements
    # Change B82(C-65) W56 H83
    # Or B82 W56 H83
    # To 82-56-83
    measurement = None
    if len(ddSection[base+4].contents) == 2:
        measurementSection = ddSection[base+4].contents[1]
        #print(measurementSection)
        matches = re.findall(r'B\d+|W\d+|H\d+', measurementSection)
        #print(matches)
        if len(matches) == 3:
            B = matches[0][1:]
            W = matches[1][1:]
            H = matches[2][1:]
            measurement = B + '-' + W + '-' + H
            print(measurement)
    return [av_ID+10000, av_name, birthdate, birthplace, height, bloodType, measurement]

try:
    con = db.connect('../AV.db')
    print("Coneect to ../AV.db")
    cur = con.cursor()
        
    for file in glob.glob("*"): 
        f = codecs.open(str(file), "r", "utf-8")
        if f == None:
            conitnue
        print("processing file: " + str(file))
        content = f.read()
        
        soup = BeautifulSoup(content);
        result = get_actressInfo(soup, int(file)) 
        if result == None:
            continue
        # update result to DB
        print(result)
        w.updateResultToDB(cur, result)
        f.close()
        con.commit()
        os.rename(file, '../proceed/' + file)
except db.Error, e:
    if con:
        con.rollback()
    print("Error %s" % e.args[0])
    sys.exit(1)
finally:
    if cur:
        cur.close()
    if con:
        con.close()
#    # download image
#    photo = soup.find('div', {"class": "photo"})
#    if photo != None:
#        imgTag = soup.find('img')
#        if imgTag != None:
#            imgsrc = imgTag['src']
#            print(imgsrc)
#            img_path = "../image/" + str(file)
#            dl.download_url(imgsrc, img_path)
#    # download itemBox
#    prefix = "http://xcity.jp" 
#    items = soup.find_all('div', {"class": "x-itemBox-package"})
#    for item in items:
#        url = item.find('a')
#        if url == None:
#            continue;
#        url = prefix + url['href']
#        print(url)
#        download_path = "../video/" + url.split('?id=')[1]
#        dl.download_url(url, download_path)
