# -*- coding: utf-8 -*- 
#
#
# for film table
#   parse product_id, title, company, release_date
# for tag
# for tag_id
# for actress_film
from bs4 import BeautifulSoup
import sqlite3 as db
import sys
import urllib2
import codecs
import re
import glob, os
import download as dl
import toSqlite as w
os.chdir("video");
# return [film_name, av_name, company, release_date, real_product_id, film_tags]
def get_filmInfo(soup, av_ID):
    
    title = soup.find('span', {"id": "program_detail_title"})
    if title == None:
        print("Title is empty, skip")
        return None
    film_name = title.string
    print(film_name)

    content_section = soup.find('div', {"class": "content"})
    if content_section == None:
        return None
        
    av_name = None
    av_name_section = content_section.find('li', {"id": "program_detail_credit"})
    if av_name_section != None:
        if av_name_section.find('a') != None:
            av_name = av_name_section.find('a').string
        else:
            av_name = av_name_section.string
        print(av_name)

    company = None
    company_span = content_section.find('span', {"id": "program_detail_label_name"})
    if company_span != None:
        company = company_span.string
        print(company)

    release_date = None
    release_date_span = content_section.find('span', text=re.compile(u'発売日'))
    if release_date_span != None:
        if len(release_date_span.parent.contents) == 2:
            release_date = release_date_span.parent.contents[1].strip().replace('/','-')
            print(release_date)
    
    product_id = None
    real_product_id = None
    product_prefix = None
    product_id_span = content_section.find('span', text=re.compile(u'品番'))
    if product_id_span != None:
        if len(product_id_span.parent.contents) == 3:
            product_id = product_id_span.parent.contents[2].strip()
            match = re.match(r'^([a-zA-Z]+).*$', product_id)
            if match == None:
                real_product_id = product_id
            else:
                for prefix in match.groups():
                    real_product_id = product_id.replace(prefix, prefix+'-')
                    product_prefix = prefix
            print(real_product_id)
    film_tags = []
    tag_section = content_section.find('span', text=re.compile(u'ジャンル'))
    if tag_section != None:
        tags = tag_section.parent.find_all('a')
        for tag in tags:
            tagString = tag.string.strip()
            film_tags.append(tagString)
            print(tagString),
        print('\n');
    
    return [film_name, av_name, company, release_date, real_product_id, film_tags]


#    return [av_ID+10000, av_name, birthdate, birthplace, height, bloodType, measurement]



# get photo
def getPhoto(soup):
    photo_section = soup.find('div', {"class": "photo"})
    if photo_section != None:
        tn_section = photo_section.find('p', {"class": "tn"})
        if tn_section != None:
            # May have no photo
            if tn_section.find('a') == None: 
                return None
            url = tn_section.a.img['src'].split('?width')[0]
            if 'noimage.gif' in url:
                return None
            download_path = "../video_img/" + str(av_ID) + ".jpg"
            dl.download_url(url, download_path)

#w.create_tag_film_table('../AV.db')

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
        result = get_filmInfo(soup, int(file)) 
#if result == None:
#            f.close()
#            continue
        # update result to DB
#        print(result)
        w.updateResultToDB(cur, result)
        f.close()
        con.commit()
        os.rename(file, '../proceed_video/' + file)
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
