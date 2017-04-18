# Rapidgator links to DownloadStation Feeder
#
# Given a list of rapidgator file list, feed them into download station
import sys
from ds_get import download_station
from rapid_identifier import rapidQQ
import time
import var

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

    qq = rapidQQ(var.rapid_usr, var.rapid_passwd)
    ds = download_station(var.ds_ip, var.ds_port, var.ds_acct, var.ds_passwd)
    count = 0
    incr = 60
    for line in lines:
        if len(line) == 0:
            continue
        print("Processing '{}'".format(line[:-1]))
        url = qq.extract_url(line[:-1])
        if url == None:
            continue
        ds.download(url, var.ds_destination_path)
        print("{} submitted.".format(url))
        time.sleep(incr)
        incr += 30
