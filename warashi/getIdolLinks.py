from bs4 import BeautifulSoup
import urllib2
import codecs

# Similar to wget
# But using wget will get 403 Forbidden
def download_url(url, path_to_save):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    req = urllib2.Request(url, headers=hdr)
    
    try:
        content = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
    
    f = codecs.open(path_to_save, 'wb')
    f.write(content.read())
    f.close()

# print the title
for fileId in range(1, 46):
    
    f = codecs.open("page/" + str(fileId), "r", "utf-8")
    if f == None:
        conitnue
    print("processing file" + str(fileId))
    content = f.read()
    
    soup = BeautifulSoup(content);

    mainSection = soup.find('div', {"class": "cadre"})
    if mainSection == None:
        continue;
    
    url_prefix = "http://warashi-asian-pornstars.fr"

    couleur1 = mainSection.find_all('figure', {"class": ["alternance-couleur-1", "alternance-couleur-2"]}) 
    for i in couleur1:
        link = i.find('a')['href']
        avId = link.rsplit('/',1)[1]
        print("Processing AV ID = " + str(avId))
        link_url = url_prefix + link
        img_url = url_prefix + i.find('img')['src']
    
        download_url(link_url, "IdolPage/" + str(avId))
        download_url(img_url, "image/" + str(avId) + ".jpg")

    f.close()
