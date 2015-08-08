import sqlite3 as db
import sys

dbName = "AV.db"

def create_all_table(dbName):
    try:
        con = db.connect(dbName)
    
        cur = con.cursor()
# create table actress (av_ID PRIMARY KEY AUTOINCREMENT, real_name, eng_name);
        cur.execute("create table actress ( \
                        av_ID INTEGER NOT NULL PRIMARY KEY, \
                        real_name TEXT, \
                        eng_name TEXT \
                    )")
# Multiple av_ID may refer to same info (Aliases)
        cur.execute("create table actressInfo ( \
                        info_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                        birthdate TEXT, \
                        birthplace TEXT, \
                        height INTEGER, \
                        weight INTEGER, \
                        blood_type TEXT, \
                        measurements TEXT, \
                        link_ID INTEGER, \
                        tag_ID INTEGER \
                    )")

        cur.execute("create table film ( \
                        film_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                        title_orig TEXT, \
                        title_eng TEXT, \
                        company TEXT \
                    )")
        
        cur.execute("create table tag ( \
                        tag_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                        name TEXT NOT NULL \
                    )")
        
        cur.execute("create table av_link ( \
                        link_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                        address TEXT NOT NULL \
                    )")
        
        cur.execute("create table actress_info ( \
                        av_ID INTEGER NOT NULL, \
                        info_ID INTEGER NOT NULL \
                    )")
        
        cur.execute("create table actress_link( \
                        av_ID INTEGER NOT NULL, \
                        link_ID INTEGER NOT NULL \
                    )")
        
        cur.execute("create table actress_alias ( \
                        av_ID INTEGER NOT NULL, \
                        alias_ID INTEGER NOT NULL \
                    )")
        
        cur.execute("create table actress_film ( \
                        av_ID INTEGER NOT NULL, \
                        film_ID INTEGER NOT NULL \
                    )")
        
        cur.execute("create table actress_tag ( \
                        av_ID INTEGER NOT NULL, \
                        tag_ID INTEGER NOT NULL \
                    )")
        
        cur.execute("create table film_tag ( \
                        film_ID INTEGER NOT NULL, \
                        tag_ID INTEGER NOT NULL \
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
    cur.execute('insert or replace into actress values (?,?,?)', data) 
#  2. For actressInfo
def insert_actressInfo(cur, data):
    cur.execute('insert or replace into actressInfo values (?,?,?,?,?,?,?,?,?)', data)
#  3. For film
#  4. For tag
#  5. For actress_info
#  6. For actress_alias
#  7. For actress_link
#  8. For actress_film
#  9. For actress_tag
# 10. For film_tag
# 11. For av_link
#


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
