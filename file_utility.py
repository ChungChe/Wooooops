# Scan folder Sorted/

import os
import sys
import scandir
import sqlite3 as db

reload(sys)
sys.setdefaultencoding('utf-8')

class file_holder:
    def to_gb_str(self, val):
        return float(val) / 1073741824
    def show_possible_match(self, search_str, show_path=False):
        command = 'select name, file_size, full_path from files where name LIKE "%{}%" or full_path LIKE "%{}%"'.format(search_str, search_str)
        try:
            self.__cur.execute(command)
            match = self.__cur.fetchall()
            if match == []:
                print('Not Found')
                return
            total_size = 0
            match.sort()
            for m in match:
                total_size += m[1]
                if show_path == False:
                    print("{:7.2f} GB   {} ".format(self.to_gb_str(m[1]), m[0]))
                else:
                    print("{:7.2f} GB   {} {}".format(self.to_gb_str(m[1]), m[0], m[2]))
            print('===== records: {}, total: {:.2f} GB ========================'.format(len(match), self.to_gb_str(total_size)))
        except Exception as e:
            print("Exception in search {}, {}".format(search_str, e))

    def is_file_exists(self, file_name):
        self.__cur.execute('select name from files where name=:NAME COLLATE NOCASE', {'NAME': file_name})
        match = self.__cur.fetchall()
        if match == []:
            return False
        return True
    def create_table_if_not_exists(self):
        try:
            self.__cur.execute("create table if not exists files (\
                name TEXT, \
                ext TEXT, \
                file_size integer, \
                full_path TEXT, \
                PRIMARY KEY (name, file_size, ext) \
                )")
            self.__con.commit()
        except Exception as e:
            print("Exception in create_table {}".format(e))
            if self.__con:
                self.__con.rollback()
    def insert(self, packed_data):
        try:
            self.__cur.execute('insert or ignore into files values (?,?,?,?)', packed_data)
            self.__con.commit()
        except Exception as e:
            print("Exception in insert, {}".format(e))
            if self.__con:
                self.__con.rollback()
    def scan(self, path):
        if not os.path.exists(path):
            print('Path not exists: {}'.format(path))
            return
        for entry in scandir.scandir(path):
            ep = entry.path
            if entry.is_dir(follow_symlinks=False):
                for e in self.scan(ep):
                    yield e
            else:
                #print(ep)
                try:
                    statinfo = os.stat(entry.path)
                    size = statinfo.st_size
                    fn = entry.path.split("/")[-1] 
                    ext = fn.split(".")[-1]
                    base = fn.replace(".{}".format(ext), "")
                    if not self.is_mov_format(ext):
                        continue
                    #print(fn)
                    packed_data = [base.decode('utf-8'), ext, size, entry.path.decode('utf-8')]
                    print(packed_data)
                    self.insert(packed_data)
                except Exception as e:
                    print("Exception in scan {}, {}".format(entry.path, e))
                    continue
    def is_mov_format(self, file_name):
        f = ['mp4', 'wmv', 'avi', 'mov', 'mpg', 'mpeg', 'mkv', 'rmvb', 'rm', 'flv', 'm4v']
        for e in f:
            if e in file_name:
                return True
        return False
    def scan_all(self, path):
        entries = self.scan(full_path)
        for entry in entries:
            pass
    def __init__(self, path=None):
        self.__db_name = "my_files.db"
        self.__con = db.connect(self.__db_name)
        self.__con.execute("PRAGMA journal_mode=WAL")
        self.__cur = self.__con.cursor()
        if path == None:
            return
        self.create_table_if_not_exists()
        self.scan_all(path)

    def __exit__(self):
        if self.__cur:
            self.__cur.close()
        if self.__con:
            self.__con.close()
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} folder".format(sys.argv[0]))
        sys.exit()
    full_path = os.path.expanduser(sys.argv[1])
    h = file_holder(full_path)
    
    '''
    h = file_holder()
    print(h.is_file_exists("abp-100"))
    print(h.is_file_exists("ABP-100"))
    '''
