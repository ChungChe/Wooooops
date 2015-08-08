import sqlite3 as db
import sys

dbName = "AV.db"

def create_all_table(dbName):
    try:
        con = db.connect(dbName)
    
        cur = con.cursor()
# create table actress (av_ID PRIMARY KEY AUTOINCREMENT, real_name, eng_name);
        cur.execute("create table actress ( \
                        av_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                        real_name TEXT, \
                        eng_name TEXT, \
                        warashi_id INTEGER \
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
                        blog TEXT, \
                        twitter TEXT \
                    )")

        cur.execute("create table film ( \
                        film_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                        title_orig TEXT, \
                        title_eng TEXT, \
                        company TEXT \
                    )")
        
        cur.execute("create table tag( \
                        tag_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                        name TEXT NOT NULL \
                    )")
        
        cur.execute("create table actress_info ( \
                        av_ID INTEGER NOT NULL, \
                        info_ID INTEGER NOT NULL \
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


#def insert_actress_info_from_csv(csv):
# insert info actress ( \
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
create_all_table(dbName)
