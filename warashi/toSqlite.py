import sqlite3 as db
import sys

dbName = "AV.db"

def create_all_table(dbName):
    try:
        con = db.connect(dbName)
    
        cur = con.cursor()
# create table actress, info_ID is for many to one mapping
        cur.execute("create table actress ( \
                        av_ID INTEGER NOT NULL PRIMARY KEY, \
                        real_name TEXT, \
                        eng_name TEXT, \
                        info_ID INTEGER REFERENCES actressInfo(info_ID) \
                    )")
# Multiple av_ID (Aliases) may refer to same info, this is many to one mapping
# At begin av_ID === info_ID, but av_ID has alias ID (with ID > 20000)
        cur.execute("create table actressInfo ( \
                        info_ID INTEGER NOT NULL PRIMARY KEY, \
                        birthdate TEXT, \
                        birthplace TEXT, \
                        height INTEGER, \
                        weight INTEGER, \
                        blood_type TEXT, \
                        measurements TEXT \
                    )")

        cur.execute("create table film ( \
                        film_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                        product_id TEXT UNIQUE, \
                        title TEXT UNIQUE, \
                        company TEXT, \
                        release_date TEXT \
                    )")

        cur.execute("create table tag ( \
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                        name TEXT UNIQUE \
                    )")
        # Many to many mapping
        # tag to ID mapping, ID here can be av_ID, film_ID 
        cur.execute("create table tag_id ( \
                        tag_id INTEGER REFERENCES tag(id), \
                        id INTEGER NOT NULL \
                    )")
        # Many to one mapping, multiple links refer to the same person's info
        cur.execute("create table link_info ( \
                        link_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                        address TEXT NOT NULL UNIQUE, \
                        info_ID INTEGER REFERENCES actressInfo(info_ID) \
                    )")
        # Many to many mapping, film_ID starts from 50000 
        cur.execute("create table actress_film ( \
                        av_ID INTEGER REFERENCES actress(av_ID), \
                        film_ID INTEGER REFERENCES film(film_ID) \
                    )")
        
        con.commit()
    
    except db.Error, e:
        if con:
            con.rollback()
        print("Error %s:" % e.args[0])
        sys.exit(1)
    finally:
        if con:
            con.close()

#  1. For actress
def insert_actress(cur, data):
    cur.execute('insert or ignore into actress values (?,?,?,?)', data) 
#  2. For actressInfo
def insert_actressInfo(cur, data):
    cur.execute('insert or ignore into actressInfo values (?,?,?,?,?,?,?)', data)
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

#def insert_actress_info_from_csv(csv):
# insert into actress ( \
#                           real_name, \
#                           eng_name, \
#                           birthdate, \
#                           birthplace, \
#                           height, \
#                           weight, \
#                           blooc_type, \
#                           measurements, \
#                           blog, \
#                           twitter \
#                     ) values ("...", "...",...);
#
#create_all_table(dbName)
