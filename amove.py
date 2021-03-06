#!/usr/bin/env python3
# mv a file "SHKD-548.avi" to prefix_path/S/SHKD/SHKD-548/SHKD-548.avi
# mv file to path/file
import os
import re
import sys
import ntpath
import scandir
import errno
import shutil

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
    if base_name == None:
        print("Error: base name '{}' is empty, from: '{}".format(base_name, file_name))
        return
    #print('Abs path: ' + abs_from_path)
    
    # RKI-076A.mp4 --> RKI-076
    product_id = ""
    match1 =  re.match(r'^([A-Z0-9]+-[A-Z]*\d+)\D*\.\w', base_name)
    if match1 != None:
        for gg in match1.groups():
            product_id = gg
    if product_id == "":
        print("Error: cannot find product id from: {}".format(base_name))
        return
    match =  re.match(r'^([A-Z0-9]+)-[A-Z]*\d+.*$', base_name)
    if match == None:
        return
    #print('filename: ' + base_name)
    for product_prefix in match.groups():
        if product_prefix == None:
            return
        #print('product prifix: ' + product_prefix)
        # check from
        # prefix_path/S/SHKD/SHKD-548/SHKD-548A.avi
        to_path = "{}/{}/{}/{}/{}".format(abs_to_path, product_prefix[0], product_prefix, product_id, base_name)
        if os.path.isfile(to_path):
            print("File '{}' exists: in '{}', abort.".format(abs_from_path, to_path))
            return
        if not os.path.exists(abs_from_path):
            print("From file: {} dosn't exist".format(abs_from_path))
            return
        # if folder not exists, create one
        dir_name = os.path.dirname(to_path) 
        #print("dir name: {}".format(dir_name))
        if not os.path.exists(dir_name):
            #print("dir name '{}' not exists, create one!".format(dir_name))
            os.makedirs(dir_name)
        # file exists in to path, abort
        if os.path.exists(to_path):
            print("{} already exists, abort.".format(to_path))
            return
        print("'{}' -> '{}'".format(abs_from_path, to_path))
        try:
            command = "mv {} {}".format(abs_from_path, to_path)
            os.system(command)
            #os.rename(abs_from_path, to_path) 
            #shutil.move(abs_from_path, to_path)
        except OSError as e:
            if e.errno == errno.EEXIST:
                print("Exception: file exists")
            elif e.errno == 14:
                print("QQ")
            else:
                raise
        except Exception:
            pass

def list_folder_files(path):
    if not os.path.exists(path):
        print('Path not exists: {}'.format(path))
        return
    folder_files = []
    for file_name in os.listdir(path):
        if os.path.isfile(os.path.join(path, file_name)):
            folder_files.append(file_name)
    return folder_files

def walk(path):
    file_list = []
    for path, dirnames, filenames in os.walk(path):
        for name in filenames:
            final_name = os.path.abspath(os.path.join(path, name))
            if os.path.exists(final_name):
                file_list.append(final_name)
    return file_list

def scantree(path):
    if not os.path.exists(path):
        print('Path not exists: {}'.format(path))
        return
    for entry in scandir.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)  # see below for Python 2.x
        else:
            yield entry

def move_all_files(from_path, to_path):
    print("FROM: {}".format(from_path))
    print("TO: {}".format(to_path))
    #files = list_folder_files(from_path)
    entries = scantree(from_path)
    #entries = walk(from_path)

    for entry in entries:
        move_single_file(entry.path, to_path)
        #move_single_file(entry, to_path)
        #move_single_file(from_path + file_name, to_path)

# amove from to
if len(sys.argv) < 3:
    print('Usage: amove from to')
    sys.exit()

move_all_files(os.path.expanduser(sys.argv[1]), os.path.expanduser(sys.argv[2]))

#move_single_file(sys.argv[1], sys.argv[2])
