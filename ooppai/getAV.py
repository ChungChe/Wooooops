from bs4 import BeautifulSoup
import urllib2
import codecs
import re
# Data to CSV

f1 = codecs.open("av.csv", "w+", "utf-8")
# print the title
f1.write('Avatar,Real Name,English Name,Aliases,Birthdate,Birthplace,Height,Weight,Blood Type,Measurements,Blog,Twitter\n')
for fileId in range(1, 668):
    
    f = codecs.open(str(fileId), "r", "utf-8")
    if f == None:
        conitnue
    print("processing file" + str(fileId))
    content = f.read()
    
    soup = BeautifulSoup(content);
    
    if soup.find('h1', text="404 Not Found") != None:
        continue;
    # 0. ID (image link)
    f1.write('<img src=/image/'+str(fileId)+'.jpg></img>,')
    # 1. Real name
    real_name_list = soup.find_all('h2', {"itemprop": "alternateName"})
    for real_name in real_name_list:
        f1.write('\"'+real_name.string+'\"')
    f1.write(',')
    
    # 2. English name
    englisth_name_list = soup.find_all('h1', {"itemprop": "name"})
    for eng_name in englisth_name_list:
        f1.write('\"'+eng_name.string+'\"')
    f1.write(',')
    
    infos = soup.find_all('div', {"class": "Info"})
    for info in infos:
    
        # 3. Aliases 
        th_alias = info.find('th', text="Aliases")
        if th_alias != None:
            alias = th_alias.parent.find('span')
            f1.write('\"'+alias.string+'\"')
        f1.write(',')
    
        # 4. Birthdate 
        birthdate = info.find('span', {"itemprop": "birthDate"})
        if birthdate != None:
            f1.write('\"'+birthdate.string+'\"')
        f1.write(',')
    
        # 5. Birthplace 
        th_birthplace = info.find('th', text="Birthplace")
        if th_birthplace != None:
            birthplace = th_birthplace.parent.find('td')
            f1.write('\"'+birthplace.string+'\"')
        f1.write(',')
        
        # 6. Height 
        th_height = info.find('th', text="Height")
        if th_height != None:
            height = th_height.parent.find('td')
            f1.write('\"'+height.string+'\"')
        f1.write(',')
        
        # 7. Weight 
        th_weight = info.find('th', text="Weight")
        if th_weight != None:
            weight = th_weight.parent.find('td')
            f1.write('\"'+weight.string+'\"')
        f1.write(',')
        
        # 8. Blood Type 
        th_bloodType = info.find('th', text="Blood type")
        if th_bloodType != None:
            bloodType = th_bloodType.parent.find('td')
            f1.write('\"'+bloodType.string+'\"')
        f1.write(',')
        
        # 9. Measurements 
        th_measurement = info.find('th', text="Measurements")
        if th_measurement != None:
            measurement = th_measurement.parent.find('td')
            f1.write('\"'+measurement.string+'\"')
        f1.write(',')
    
    # 10. Blog 
    blog = soup.find('a', {"itemprop": "url"})
    if blog != None:
        f1.write('<a href='+blog['href']+'>link</a>')
    f1.write(',')
    # 11. Twitter 
    twitter = soup.find('a', {"href":re.compile('twitter.com')})
    if twitter != None:
        f1.write('<a href='+twitter['href']+'>link</a>')
    f1.write('\n')
    
    #    titles = info.find_all('dic', {"class":"entry-title"})
    #    for title in titles:
    #        f1.write title.get_text(' ', strip=True)
    #    f1.write("===============================================")
    #    # This is current page's tag
    #    tags = info.find_all(lambda tag: tag.name == 'a' and tag.get('rel') == ['tag'])
    #    for tag in tags:
    #        f1.write tag.get_text(' ', strip=True)
    #    f1.write("------------------------------------------------")
    
    #f1.write(data)
    #f1.close()
    
    #f1.write(soup.find_all('div', class_='title'))
    f.close()
f1.close()
