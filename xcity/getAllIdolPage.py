from bs4 import BeautifulSoup
import download as dl

# print the title
for fileId in range(1, 7883):
    url = "http://xcity.jp/idol/detail/?id=%d" % fileId
    print("download: " + url)
    
    dl.download_url(url, "page/" + str(fileId))

