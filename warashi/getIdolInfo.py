from bs4 import BeautifulSoup
import urllib2
import codecs
import re
import glob, os
os.chdir("IdolPage");

for file in glob.glob("2029"): 
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

    print(real_name),
    print(eng_name)
    
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

    # Get Birthdate
    birthdate = soup.find('time', {"itemprop": "birthDate"})
    if birthdate != None:
        print(birthdate['content'])

    # Get Birthplace
    birthplace = soup.find('span', {"itemprop":"addressRegion"})
    if birthplace != None:
        print(birthplace.string)
    # Get Height
    heightSection = soup.find('p',{"itemprop":"height"})
    if heightSection != None:
        height = heightSection.find('span',{"itemprop":"value"})
        if height!= None:
            print(height.string)
    # Get Weight
    weightSection = soup.find('p',{"itemprop":"weight"})
    if weightSection != None:
        weight = weightSection.find('span',{"itemprop":"value"})
        if weight!= None:
            print(weight.string)
    # Get Blood Type
    for bloodTypeSection in soup(text=re.compile('blood type')):
        bloodType = bloodTypeSection.rsplit(': ')[1]
        print(bloodType)
    # Get Measurements
    for measurementSection in soup(text=re.compile('measurements:')):
        measurementTemp = measurementSection.rsplit(': JP ')[1]
        measurement = measurementTemp.rsplit('(US')[0]
        print(measurement)
    # Get Blog
    blogSection = soup.find('div', {"id":"pornostar-profil-liens"})
    if blogSection != None:
        blogs = blogSection.find_all('a')
        for blog in blogs:
            print(blog['href'])
    # Get Twitter

    # Tags
    tagSection = soup.find('p', {"class": "implode-tags"})
    if tagSection != None:
        tags = tagSection.find_all('a')
        for tag in tags:
            print(tag.string)

    f.close()
