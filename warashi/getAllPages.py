from bs4 import BeautifulSoup
import urllib2
import codecs

# From page 1 to page 61
for pageId in range(1, 61):
    print("Processing page"+str(pageId))
    DOWNLOAD_URL = "http://warashi-asian-pornstars.fr/en/s-2-2/female-pornstars/categorie/2/page/" + str(pageId)
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    req = urllib2.Request(DOWNLOAD_URL, headers=hdr)
    
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
    
    content = page.read()
    
    soup = BeautifulSoup(content);
    
    pretty = soup.prettify()
    f = codecs.open("page/"+str(pageId), "w", "utf-8")
    f.write(pretty);
    f.close()

