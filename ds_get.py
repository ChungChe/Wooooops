# DS Get WebAPI
import os
import requests
import json
import urllib
import warnings

class download_station:
    def __init__(self, host, port, usr, passwd):
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
        self.__s = requests.Session()
        self.__s.headers = hdr
        self.__host = host
        self.__port = port
        self.__debug = True 
        self.__sid = self.get_session_id(host, port, usr, passwd)

    def get_session_id(self, host, port, usr, passwd):
        p = {'api': 'SYNO.API.Auth', 'version': '2', 'method': 'login', 'account': usr, 'passwd': passwd, 'session': 'DownloadStation', 'format': 'cookie'}
        req_get_str = 'https://{}:{}/webapi/auth.cgi'.format(host, port)
        # Since I turn off verify, so I deprecate "InsecureRequestWarning" here
        warnings.filterwarnings("ignore")
        resp = self.__s.get(req_get_str, params=p, verify=False)
        if self.__debug == True:
            print("Resp: {}".format(resp.content))
        if resp.status_code == 200:
            c = json.loads(resp.content)
            sid = c['data']['sid']
            if self.__debug == True:
                print(c['data']['sid'])
            return sid.encode("ascii", "ignore")
        else:
            print(resp.error_code)
            return None

    def download(self, uri, dest):
        p = {'api': 'SYNO.DownloadStation.Task', 'version': 1, 'method': 'create', 'uri' : uri, '_sid': self.__sid, 'destination': dest}
        if self.__debug == True:
            print(p)
        req_get_str = 'https://{}:{}/webapi/DownloadStation/task.cgi'.format(self.__host, self.__port)
        resp = self.__s.get(req_get_str, params=p, verify=False)
        status_all = json.loads(resp.content)
        status = status_all['success']
        #code = status_all['error']
        #print('Code: {}'.format(code))
        print('Status all: {}'.format(status_all))
        if self.__debug == True:
            if status == True: 
                print("Status: {}".format(status))
            else:
                print("Status: {}".format(status))
                
                #r = {'400':  'File upload failed', '401': 'Max number of tasks reached', '402':  'Destination denied', '403': 'Destination does not exist', '404': 'Invalid task id', '405': 'Invalid task action', '406': 'No default destination', '407': 'Set destination failed', '408': 'File does not exist'}
                #print("Status: {}, reason: {}".format(status, r[code]))
            #print("Status all : {}".format(status_all))

        # logout
        p_out = {'api': 'SYNO.API.Auth', 'version': 1, 'method': 'logout', 'session' : 'DownloadStation'}
        logout_str = 'https://{}:{}/webapi/auth.cpi'.format(self.__host, self.__port)
        resp_out = self.__s.get(logout_str, params=p_out, verify=False)
        #print(resp_out)
        #status_out = json.loads(resp_out.content)
        #print(status_out)
        return status

if __name__ == "__main__":
    ds = download_station('192.168.0.2', '9999', 'user', 'passwd')
    ds.download('http://some_url_file_path_to_download')
