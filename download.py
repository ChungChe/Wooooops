#import urllib
from urllib.request import Request, urlopen
#import codecs
def download_url(url, path_to_save):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
    
    try:
        content = urlopen(req)
    except urllib.error.HTTPError as e:
        pass
    
    f = open(path_to_save, 'wb')
    f.write(content.read())
    f.close()
