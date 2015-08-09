from bs4 import BeautifulSoup
import sqlite3 as db
import sys
import urllib2
import codecs
import re
import glob, os
import toSqlite
os.chdir("IdolPage");
#toSqlite.create_all_table('../AV.db')
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
    
try:
    con = db.connect('../AV.db')
    print("Connect to IdolPage/AV.db")
    cur = con.cursor()
        
    for file in glob.glob("*"): 
        warashi_avId = int(file) 
        print(warashi_avId)
        f = codecs.open(str(file), "r", "utf-8")
        if f == None:
            conitnue
        print("processing file: " + str(file))
        content = f.read()
        
        soup = BeautifulSoup(content);
    
        title = soup.find('title').string
        
        av_name= title.rsplit('/')[0].rsplit(' - ')
        eng_name = av_name[0]
        real_name = av_name[1]
        if real_name == "japanese pornstar": 
            real_name = ''
        print(real_name),
        print(eng_name)
        actress_data = [warashi_avId, real_name, eng_name, warashi_avId] 
        toSqlite.insert_actress(cur, actress_data)
    
        # Get All Aliases
        alt_name_section = soup.find('div', {"id": "pornostar-profil-noms-alternatifs"})
        if alt_name_section != None:
            aliasList = alt_name_section.find_all(itemprop = "additionalName")
            idx = 0
            for i in aliasList:    
                if (idx % 2 == 0):
                    alt_eng_name = i.string
                    print(alt_eng_name)
                else:
                    alt_real_name = i.string
                    print(alt_real_name)
                idx += 1
        actressInfo_data = get_actressInfo(soup, warashi_avId) 
        toSqlite.insert_actressInfo(cur, actressInfo_data)

        # Get links
        blogSection = soup.find('div', {"id":"pornostar-profil-liens"})
        if blogSection != None:
            blogs = blogSection.find_all('a')
            for blog in blogs:
                link = blog['href']
                link_data = [link, warashi_avId]
                toSqlite.insert_link_info(cur, link_data)
                print(link)
        # Tags
        tagSection = soup.find('p', {"class": "implode-tags"})
        if tagSection != None:
            tags = tagSection.find_all('a')
            for tag in tags:
                toSqlite.insert_tag(cur, [tag.string])
                cur.execute('select id from tag where name=:Name', {"Name": tag.string})
                tagList = cur.fetchone()
                for tagElement in tagList:
                    tag_id_data = [tagElement, warashi_avId]
                    cur.execute('select * from tag_id where tag_id=:TagID and id=:ID',
                            {"TagID": tagElement,
                             "ID": warashi_avId})
                    tagIDList = cur.fetchone()
                    if tagIDList == None:
                        toSqlite.insert_tag_id(cur, tag_id_data)
                        print(tag.string)

        # Film info
        filmTable = soup.find('table', {"class": "filmographie sortable"})
        if filmTable == None:
            continue;
        rows = filmTable.find_all('tr', {"class": "compilation"})
        if rows == None:
            continue;
        for row in rows:
            columns = row.find_all('td')
            if columns == None:
                continue;
            if columns[1].string != None:
                film_title = columns[1].string
            else:
                film_title = columns[0].string
            film_company = columns[2].string
            film_release_date = columns[4].string
            film_data = [film_title, film_company, film_release_date]
            cur.execute('select title from film where title=:T', {"T": film_title})
            film_result = cur.fetchone()
            if film_result == None:
                toSqlite.insert_film(cur, film_data)
            # update actress_film table
            # find film_id form titlem assign (av_ID, film_ID)
            cur.execute('select film_ID,title from film where title=:T', {"T": film_title})
            film_fetch = cur.fetchone()
            if film_fetch != None:
                film_ID = film_fetch[0]
                actress_film_data = [warashi_avId, film_ID]
                # make sure no data duplicated
                cur.execute('select * from actress_film where av_ID=:AVID and film_ID=:FilmID',
                    {"AVID": warashi_avId, "FilmID": film_ID})
                actress_film_fetch = cur.fetchone()
                if actress_film_fetch == None:
                    toSqlite.insert_actress_film(cur, actress_film_data)
            else:
                print('Error: cannot find title: ', film_title)
        f.close()
        con.commit()
        os.rename(file, 'proceed/' + file)
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
        
