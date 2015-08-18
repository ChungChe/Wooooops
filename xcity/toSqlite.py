import sqlite3 as db
import sys

def create_tag_film_table(dbName):
    try:
        con = db.connect(dbName)
        cur = con.cursor()
        cur.execute("create table tag_filmId ( \
                        tag_id INTEGER REFERENCES tag(id), \
                        film_id INTEGER REFERENCES film(film_ID) \
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
        

# 1. find film, if the film exists, update product_id, otherwise, create a new film
# 2. get film ID from DB
# 3. get actressID from DB
# 4. if actressID in invalid, create a new actressID & actressIDInfo
# 5. write info to actress_film
# 6. handle tags
#    find tag, if the tag is not exists, create a new tag
#    update tag
#
# [film_name, av_name, company, release_date, real_product_id, film_tags]
#     0         1         2          3                4            5
def updateResultToDB(cur, result):
    if result == None:
        return
    film_name = result[0]
    av_name = result[1]
    cur.execute('select * from film where title=:Title', {"Title": film_name})
    matchFilm = cur.fetchone()
    product_id = result[4]
    # update product_id only
    if matchFilm != None:
        film_ID = result[0]
        print('update film_ID ' + film_ID + ' with ' + product_id)
        update_product_id(cur, product_id, film_ID)
    # create new film data
    else:
        company = result[2]
        release_date = result[3]
        film_data = [product_id, film_name, company, release_date]
        insert_film_with_productId(cur, film_data)
        print('insert new row ' + str(film_data))

    cur.execute('select film_ID from film where title=:Title', {"Title": film_name})
    matchFilmId = cur.fetchone()
    filmID = None 
    for fid in matchFilmId:
        filmID = fid
    avID = None
    cur.execute('select av_ID from actress where real_name=:Name', {"Name": av_name})
    print(av_name)
    matchAVId = cur.fetchone()
    # see video 35512, skip
    if matchAVId == None:
        print('Cannot find av_name in DB, skip...')
        return None
    for aid in matchAVId:
        avID = aid
    if avID != None and filmID != None:
        actress_film_data = [aid, fid]
        insert_actress_film(cur, actress_film_data)
    # handle tags
    filmTags = result[5]
    for filmTag in filmTags:
        #print(filmTag)
        insert_tag(cur, [filmTag])
        cur.execute('select id from tag where name=:Name', {"Name": filmTag})
        tagList = cur.fetchone()
        for tagItem in tagList:
            if filmID == None:
                continue
            tag_filmId_data = [tagItem, filmID]
#print(tag_filmId_data)
            insert_tag_filmId(cur, tag_filmId_data) 
        
#    av_real_name = result[1]
#    cur.execute('select * from actress where real_name=:Name', {"Name": av_real_name})
#    matchAV = cur.fetchone()
#    if matchAV == None:
#        print(av_real_name + ' is not in the DB, create it')
#        actress_data = [result[0], result[1], result[0]]
#        print(actress_data)
#        insert_actress(cur, actress_data)
#        actressInfo_data = [result[0], result[2], result[3], result[4], result[5], result[6]]
#        insert_actressInfo(cur, actressInfo_data)
#    else:
#        print(av_real_name + 'is in the DB, no need to create')

def update_product_id(cur, product_id, film_ID):
    cur.execute('update film set product_id=? where film_ID=?', (product_id, film_ID))
def insert_film_with_productId(cur, data):
    cur.execute('insert or ignore into film (product_id, title, company, release_date) values (?,?,?,?)', data) 
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
def insert_tag_filmId(cur, data):
    cur.execute('insert or ignore into tag_filmId values (?,?)', data) 
