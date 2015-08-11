# -*- coding: utf-8 -*- 
from bs4 import BeautifulSoup
import sqlite3 as db
import sys
import urllib2
import codecs
import re
import glob, os
import download as dl
os.chdir("page");

def get_actressInfo(soup, av_ID):
    # Get Birthdate
    birthdate = None
    birthdataSection = soup.find('time', {"itemprop": "birthDate"})
    if birthdataSection != None:
        birthdate = birthdataSection['content']
        print(birthdate)
    # Get Birthplace
    birthplace = None
    birthplaceSection = soup.find('span', {"itemprop":"addressRegion"})
    if birthplaceSection != None:
        birthplace = birthplaceSection.string
        print(birthplace)

    # Get Height
    height = None
    heightSection = soup.find('p',{"itemprop":"height"})
    if heightSection != None:
        heightSpan = heightSection.find('span',{"itemprop":"value"})
        if heightSpan != None:
            height = heightSpan.string
            print(height)
    # Get Weight
    weight = None
    weightSection = soup.find('p',{"itemprop":"weight"})
    if weightSection != None:
        weightSpan = weightSection.find('span',{"itemprop":"value"})
        if weightSpan != None:
            weight = weightSpan.string
            print(weight)
            
    # Get Blood Type
    bloodType = None
    for bloodTypeSection in soup(text=re.compile('blood type')):
        bloodType = bloodTypeSection.rsplit(': ')[1]
        print(bloodType)
    # Get Measurements
    measurement = None
    for measurementSection in soup(text=re.compile('measurements:')):
        measurementTemp = measurementSection.rsplit(': JP ')
        print('size: '+str(len(measurementTemp)))
        if (len(measurementTemp) == 1):
            measurement = None
        elif (len(measurementTemp) != 2):
            measurementTemp = measurementSection.rsplit(': FR ')[1]
            measurement = measurementTemp.rsplit('(US')[0]
        else:
            measurementTemp = measurementTemp[1]
            measurement = measurementTemp.rsplit('(US')[0]
        print(measurement)
    return [av_ID, birthdate, birthplace, height, weight, bloodType, measurement]
    
        
for file in glob.glob("*"): 
    warashi_avId = int(file) 
    print(warashi_avId)
    f = codecs.open(str(file), "r", "utf-8")
    if f == None:
        conitnue
    print("processing file: " + str(file))
    content = f.read()
    
    soup = BeautifulSoup(content);
    
    title = soup.find('meta', {"property": "og:title"})
    if title == None:
        continue;
    av_name = title['content']
    name_list = re.split('\(|\)', av_name)
    # 1. Name
    if name_list != None:
        print(name_list[0])
# ------ profile section is buggy, see profile 3384 --------
#    profile = soup.find('dl', {"class": "profile"})
#    if profile != None:
#        ddSection = profile.find_all('dd')
#        # 2. Birthdate
#        birthdate = ddSection[1].contents[1]
#        birthdate = birthdate.replace(u"年","-")
#        birthdate = birthdate.replace(u"月","-")
#        birthdate = birthdate.replace(u"日","")
#
#        print(birthdate)
#        # 3. Blood type
#        bloodType = ddSection[2].contents[1]
#        bloodType = bloodType.replace(u"型","")
#        print(bloodType)
#        # 4. Birthplace
#        print(ddSection[3].contents[1])
#        # 5. Height
#        height = ddSection[4].contents[1]
#        height = height.replace("cm","")
#        print(height)
#        # 6. Measurements
#        # Change B82(C-65) W56 H83
#        # Or B82 W56 H83
#        # To 82-56-83
#        measurementSection = ddSection[5].contents[1]
#        print(measurementSection)
    # download image
    photo = soup.find('div', {"class": "photo"})
    if photo != None:
        imgTag = soup.find('img')
        if imgTag != None:
            imgsrc = imgTag['src']
            print(imgsrc)
            img_path = "../image/" + str(file)
            dl.download_url(imgsrc, img_path)
    # download itemBox
    prefix = "http://xcity.jp" 
    items = soup.find_all('div', {"class": "x-itemBox-package"})
    for item in items:
        url = item.find('a')
        if url == None:
            continue;
        url = prefix + url['href']
        print(url)
        download_path = "../video/" + url.split('?id=')[1]
        dl.download_url(url, download_path)
    os.rename(file, '../proceed/' + file)
    f.close()
