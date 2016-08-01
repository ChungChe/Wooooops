#!/usr/bin/env python3
import os
import sys
import scandir
import errno
# use find . -type d -empty -print | xargs rmdir
# Since in acd_cli rmdir will delete non-empty folders

def rm_empty_folder(path):
    #print("Path: {}".format(path))
    if not os.path.exists(path):
        print('Path not exists: {}'.format(path))
        return
    for entry in scandir.scandir(path):
        if entry.is_dir():
            rm_empty_folder(entry.path) 
            try:
                print('Remove "{}"'.format(entry.path))
                os.rmdir(entry.path)
            except OSError as e:
                pass
                #print(e)

if len(sys.argv) < 2:
    print('Usage: rm_empty_dir path')
    sys.exit()

print(sys.argv[1])
rm_empty_folder(os.path.expanduser(sys.argv[1]))
