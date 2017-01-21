# Rapidgator.net Premium Link Extractor
import os
import climber2
from bs4 import BeautifulSoup
import requests

class rapidQQ:
    def __init__(self, user, passwd):
        self.__s = self.rapid_auth(user, passwd) 
    def rapid_auth(self, user, passwd):
        s = requests.Session()
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
        s.headers = hdr
        s.post('https://rapidgator.net/auth/login', {'LoginForm[email]': user, 'LoginForm[password]': passwd, 'LoginForm[rememberMe]': '1'}).content
        return s
    def rapid_get(self, url):
        content = ""
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
        try:
            r = self.__s.get(url, headers = hdr)
            content = u''.join(r.text.decode('utf-8'))
        except Exception as e:
            print("Exception for {}, {}".format(url, e))
            return None
        return content

    def extract_url(self, url):
        c = self.rapid_get(url)
        soup = BeautifulSoup(c, "html.parser")
        sec = soup.find('div', {'class': 'text-block file-descr'})
        url = sec.find('a')
        if url == None:
            return None
        l = url['href']
        return l
# Usage
qq = rapidQQ('your_email', 'your_password')
url = qq.extract_url('rapidgator_file_url)
print(url)
