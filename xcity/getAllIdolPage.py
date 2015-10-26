from bs4 import BeautifulSoup
import download as dl

# print the title
for fileId in range(7883, 7977+1):
    url = "http://xcity.jp/idol/detail/?id=%d" % fileId
    print("download: " + url)
    
    dl.download_url(url, "page/" + str(fileId))

