# -*- coding: utf-8 -*- 
from bs4 import BeautifulSoup
import urllib2
import download as dl
import codecs
import re
import glob, os
os.chdir("actress")
for file in glob.glob(*): 
    f = codecs.open(file, "r", "utf-8")
    if f == None:
        conitnue
    print("processing file: " + file)
    content = f.read()

    soup = BeautifulSoup(content);
    avatar = soup.find('div', {"class": "avatar-box"})
    if avatar == None:
        f.close()
        continue
    infoBox = avatar.find('div', {"class": "photo-info"})
    if infoBox == None:
        f.close()
        continue
    infos = infoBox.find_all('p')
    if infos == None:
        f.close()
        continue
    print(file)
    top = None
    center = None
    bottom = None
    for info in infos:
        tmpContent = info.contents[0]
        if u"生年月日: " in tmpContent:
            birth = tmpContent.replace(u"生年月日: ", "")
            print(birth)
        if u"身長: " in tmpContent:
            height_with_cm = tmpContent.replace(u"身長: ", "")
            height = height_with_cm.replace("cm","")
            print(height)
        if u"ブラのサイズ: " in tmpContent: 
            cup = tmpContent.replace(u"ブラのサイズ: ", "")
            print("cup: " + cup)
        if u"バスト: " in tmpContent:
            top_with_cm = tmpContent.replace(u"バスト: ", "")
            top = top_with_cm.replace("cm", "")
        if u"ウエスト: " in tmpContent:
            center_with_cm = tmpContent.replace(u"ウエスト: ", "")
            center = center_with_cm.replace("cm", "")
        if u"ヒップ: " in tmpContent:
            bottom_with_cm = tmpContent.replace(u"ヒップ: ", "")
            bottom = bottom_with_cm.replace("cm", "")
        if u"出身地: " in tmpContent:
            birthPlace = tmpContent.replace(u"出身地: ", "")
            print(birthPlace)
    if top != None and center != None and bottom != None:
        print(str(top) + "-" + str(center) + "-" + str(bottom))

                

    os.rename(file, "/home/pi/avartar/javbus/proceed_actress/" + str(file))
    f.close()
