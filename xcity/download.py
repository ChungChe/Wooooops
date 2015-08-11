import urllib2
import codecs
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
