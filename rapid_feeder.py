# Rapidgator links to DownloadStation Feeder
#
# Given a list of rapidgator file list, feed them into download station
# When 5 files are feed, wait 10 minutes for the next 5 files
import sys
from ds_get import download_station
from rapid_identifier import rapidQQ
import time

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: rapid_feeder file')
        sys.exit()
    lines = []
    try:
        with open(sys.argv[1]) as f:
            lines = f.readlines()
    except Exception as e:
        print("Exception for {}, {}".format(sys.argv[1], e))

    qq = rapidQQ('rapid_email', 'rapid_passwd')
    ds = download_station('192.168.0.2', '8888', 'ds_user', 'ds_passwd')
    count = 0
    for line in lines:
        url = qq.extract_url(line)
        if url == None:
            continue
        ds.download(url, 'destination_folder')
        count += 1
        if count == 5:
            count = 0
            time.sleep(600)
