#import urllib
from urllib.request import Request, urlopen
#import codecs
def download_url(url, path_to_save):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
    content = ""    
    try:
        content = urlopen(req)
    except Exception:
        print("Download {} failed".format(path_to_save))
        return

    f = open(path_to_save, 'wb')
    f.write(content.read())
    f.close()
