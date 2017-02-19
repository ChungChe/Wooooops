# web interface flask backend
import sys
from gevent.wsgi import WSGIServer
from flask import Flask, render_template, abort, make_response, request, json, Response, redirect
from functools import wraps, update_wrapper

#import json
import upjav_hunter as up
import time
import timeit
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
db_name = "upjav170218.db"

avail = 0

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
        global avail
        print("Avail = {}".format(avail))
        u = up.upjav_hunter(db_name)
        ss = '"%{}%"'.format(search_string)
        #condition = '(pid LIKE {} OR title LIKE {} OR actress LIKE {} OR rapid_link LIKE {}) and length(rapid_link) > 0 and available is {}'.format(ss, ss, ss, ss, avail)
        condition = '(pid LIKE {} OR title LIKE {} OR actress LIKE {} OR rapid_link LIKE {}) and available is {}'.format(ss, ss, ss, ss, avail)
        my_dict_list = u.query_data(condition)
        if my_dict_list == None:
            return []
        print("{} Matched".format(len(my_dict_list)))
        return my_dict_list
    except Exception as e:
        print("Error: {}".format(e))

def get_recent_post():
    try:
        global avail
        print("Avail = {}".format(avail))
        u = up.upjav_hunter(db_name)
         
        today = datetime.now().date()
        five_days_before = today - timedelta(days=1)
        #condition = "post_date between '{}' and '{}' and length(rapid_link) > 0 and available is {}".format(five_days_before, today, avail)
        #condition = "post_date between '{}' and '{}' and available is {}".format(five_days_before, today, avail)
        condition = "post_date between '{}' and '{}'".format(five_days_before, today)
        start = timeit.default_timer()
        my_dict_list = u.query_data(condition)
        end = timeit.default_timer()
        print("Query takes {} seconds".format(end - start))
        if my_dict_list == None or my_dict_list == []:
            return []
        print("{} Matched".format(len(my_dict_list)))
        return my_dict_list
    except Exception as e:
        print("Error: {}".format(e))
@app.route('/submit', methods=['POST'])
@nocache
def submit():
    my_json = request.json
    body = "{}"
    if my_json != None:
        pid = my_json.get('pid')
        print("Get PID from client '{}'".format(pid))
    return Response(body, 200, mimetype = "application/json")

@app.route('/post', methods=['POST'])
@nocache
def post():
    global avail
    my_json = request.json
    body = ""
    if my_json != None:
        exists = my_json.get('exists')
        if exists:
            avail = 1
        else:
            avail = 0
        search_str = my_json.get('search_str')
        ary1 = {'url': search_str}
        print(exists, search_str)
        body = json.dumps(ary1)
        print("Body: {}".format(body))
    return Response(body, 200, mimetype = "application/json") 
    

@app.route('/')
@nocache
def home():
    my_dict_list = get_recent_post()
    if my_dict_list == None:
        my_dict_list = []
    return render_template('index.html', packed_data=my_dict_list)

@app.route('/search/<string:path>')
@nocache
def query(path):
    print("Current path = '{}'".format(path))
#    if path == 'favicon.ico': 
#        return render_template('index.html', packed_data=[])
#    else:    
    my_dict_list = search_db(path)
    if my_dict_list == None:
        my_dict_list = []
    return render_template('index.html', packed_data=my_dict_list)

if __name__ == '__main__':
    http_server = WSGIServer(('', 9487), app)
    http_server.serve_forever()
