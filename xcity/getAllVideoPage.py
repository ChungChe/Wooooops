from bs4 import BeautifulSoup
import download as dl
import os.path
# print the title
for fileId in range(1, 62490+1):
    if os.path.isfile("video/" + str(fileId)):
        continue;
    url = "http://xcity.jp/release/detail/?id=%d" % fileId
    print("download: " + url)
    
    dl.download_url(url, "video/" + str(fileId))

