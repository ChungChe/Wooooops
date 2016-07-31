# Auto Apen move
# Manual naming Apen to product ID
# 
# Example:
#   Apen File Name: SNIS-999
#   It will be moved to /somepath/SNIS
import glob, os
import re
os.chdir("/Volumes/apen")
for file1 in glob.glob("*"):
    # Exact match
    match = re.match(r'^([A-Z]+)-\d+.*$', file1)
    if match != None: 
        print('file: '+ file1)
        for prefix in match.groups():
            print(prefix)
            # moving this file1 to correct place
            # 1. if the folder is not exists, create it
            path = '/Volumes/apen/0013Amazon/0013Amazon/' + prefix
            if not os.path.exists(path):
                os.makedirs(path)
            # 2. move
            print('move ' + file1 + ' to ' + path + '/' + file1)
            os.rename(file1, path + '/' + file1) 
