#!/usr/bin/env python
# mv a file "SHKD-548.avi" to prefix_path/S/SHKD/SHKD-548.avi
# mv file to path/file
import os
import re
import sys
import ntpath

def move_single_file(file_name, prefix_path):
    #if not os.path.isfile(file_name):
    #    print('from_path is invalid: {}'.format(file_name))
    #    return
    if not os.path.exists(prefix_path):
        print('to_path is invalid: {}'.format(prefix_path))
        return
    abs_from_path = os.path.abspath(file_name)
    abs_to_path = os.path.abspath(prefix_path)
    base_name = ntpath.basename(abs_from_path)
    print('Abs path: ' + abs_from_path)
    
    match =  re.match(r'^([A-Z]+)-\d+.*$', base_name)
    if match == None:
        return
    print('filename: ' + base_name)
    for product_prefix in match.groups():
        if product_prefix == None:
            return
        print('product prifix: ' + product_prefix)
        # check from
        # prefix_path/S/SHKD/SHKD-548.avi
        to_path = "{}/{}/{}/{}".format(abs_to_path, product_prefix[0], product_prefix, base_name)
        if os.path.isfile(to_path):
            print("File exists, abort.")
            return
        print("move '{}' to '{}'".format(base_name, to_path))

def list_folder_files(path):
    if not os.path.exists(path):
        print('Path not exists: {}'.format(path))
        return
    folder_files = []
    for file_name in os.listdir(path):
        if os.path.isfile(os.path.join(path, file_name)):
            folder_files.append(os.path.abspath(file_name))
    return folder_files

def move_all_files(from_path, to_path):
    files = list_folder_files(from_path)
    for file_name in files:
        move_single_file(file_name, to_path)

# amove from to
if len(sys.argv) < 3:
    print('Usage: amove from to')
    sys.exit()

move_all_files(sys.argv[1], sys.argv[2])

#move_single_file(sys.argv[1], sys.argv[2])
