# Rapidgator.net Premium Link Extractor
import os
from bs4 import BeautifulSoup
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class rapidQQ:
    def __init__(self, user, passwd):
        
        self.__h = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
        self.__s = self.rapid_auth(user, passwd)
        self.__debug = False 
    def rapid_auth(self, user, passwd):
        s = requests.Session()
        s.headers = self.__h 
        s.post('https://rapidgator.net/auth/login', {'LoginForm[email]': user, 'LoginForm[password]': passwd, 'LoginForm[rememberMe]': '1'}).content
        return s
    def rapid_get(self, url):
        content = ""
        try:
            r = self.__s.get(url, headers = self.__h)
            content = u''.join(r.text.decode('utf-8'))
        except Exception as e:
            print("Exception for {}, {}".format(url, e))
            return None
        if self.__debug == True:
            print(content)
        return content

    def extract_url(self, url):
        c = self.rapid_get(url)
        if c == None:
            return None
        soup = BeautifulSoup(c, "html.parser")
        sec = soup.find('div', {'class': 'text-block file-descr'})
        url = sec.find('a')
        if url == None:
            return None
        l = url['href']
        return l

qq = rapidQQ('your_email', 'your_password')
url = qq.extract_url('http://rapidgator.net/file/your_file.html')
print(url)
