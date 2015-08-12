import sqlite3 as db
import sys

def updateResultToDB(cur, result):
    if result == None:
        return
    av_real_name = result[1]
    cur.execute('select * from actress where real_name=:Name', {"Name": av_real_name})
    matchAV = cur.fetchone()
    if matchAV == None:
        print(av_real_name + ' is not in the DB, create it')
        actress_data = [result[0], result[1], result[0]]
        print(actress_data)
        insert_actress(cur, actress_data)
        actressInfo_data = [result[0], result[2], result[3], result[4], result[5], result[6]]
        insert_actressInfo(cur, actressInfo_data)
    else:
        print(av_real_name + 'is in the DB, no need to create')
#  1. For actress
def insert_actress(cur, data):
    cur.execute('insert or ignore into actress (av_ID, real_name, info_ID) values (?,?,?)', data) 
#  2. For actressInfo
def insert_actressInfo(cur, data):
    cur.execute('insert or ignore into actressInfo (info_ID, birthdate, birthplace, height, blood_type, measurements) values (?,?,?,?,?,?)', data)
#  3. For film
def insert_film(cur, data):
    cur.execute('insert or ignore into film (title, company, release_date) values (?,?,?)', data) 
#  4. For tag
def insert_tag(cur, data):
    cur.execute('insert or ignore into tag (name) values (?)', data) 
#  5. For tag_id 
def insert_tag_id(cur, data):
    cur.execute('insert or ignore into tag_id values (?,?)', data) 
#  6. For link_info
def insert_link_info(cur, data):
    cur.execute('insert or ignore into link_info (address, info_ID) values (?,?)', data) 
#  7. For actress_film
def insert_actress_film(cur, data):
    cur.execute('insert or ignore into actress_film values (?,?)', data) 

