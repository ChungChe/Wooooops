import os
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_content(link):
    content = ""
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    try:
        r = requests.get(link, headers=hdr)

        content = u''.join(r.text.decode('utf-8'))
    except Exception as e:
        print("Exception for {}, {}".format(link, e))
        return None
    return content
