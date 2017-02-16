# web interface flask backend
import sys
from gevent.wsgi import WSGIServer
from flask import Flask, render_template, abort, make_response
from functools import wraps, update_wrapper

import json
import upjav_hunter as up
import time
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
db_name = "upjav170124.db"

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)

def search_db(search_string):
    try:
        u = up.upjav_hunter(db_name)
        ss = '"%{}%"'.format(search_string)
        condition = '(pid LIKE {} OR title LIKE {} OR actress LIKE {} OR rapid_link LIKE {}) and length(rapid_link) > 0 and available is 0'.format(ss, ss, ss, ss)
        my_dict_list = u.query_data(condition)
        print("{} Matched".format(len(my_dict_list)))
        return my_dict_list
    except Exception as e:
        print("Error: {}".format(e))

def get_recent_post():
    try:
        u = up.upjav_hunter(db_name)
         
        today = datetime.now().date()
        five_days_before = today - timedelta(days=5)
        condition = "post_date between '{}' and '{}' and length(rapid_link) > 0 and available is 0".format(five_days_before, today)
        my_dict_list = u.query_data(condition)
        if my_dict_list == None or my_dict_list == []:
            return []
        print("{} Matched".format(len(my_dict_list)))
        return my_dict_list
    except Exception as e:
        print("Error: {}".format(e))

@app.route('/')
@nocache
def home():
    #my_dict_list = search_db("RION")
    my_dict_list = get_recent_post()
    if my_dict_list == None:
        my_dict_list = []
    return render_template('index.html', packed_data=my_dict_list)
@app.route('/<path:path>')
@nocache
def query(path):
    if path == 'favicon.ico': 
        return render_template('index.html', packed_data=[])
    my_dict_list = search_db(path)
    if my_dict_list == None:
        my_dict_list = []
    return render_template('index.html', packed_data=my_dict_list)

if __name__ == '__main__':
    http_server = WSGIServer(('', 9487), app)
    http_server.serve_forever()
