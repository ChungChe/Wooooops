# web interface flask backend
import sys
from gevent.wsgi import WSGIServer
import werkzeug.serving
from flask import Flask, render_template, abort, make_response, request, json, Response, redirect, jsonify
from functools import wraps, update_wrapper

#import json
#import upjav_hunter as up
import javip_hunter as up
import time
import timeit
from datetime import datetime, timedelta
from rapid_identifier import rapidQQ
from ds_get import download_station
import var
from javlib_handler import *

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
#db_name = "upjav170218.db"
db_name = "javip.db"

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
        #u = up.upjav_hunter(db_name)
        u = up.javip_hunter(db_name)
        ss = '"%{}%"'.format(search_string)
        #condition = '(url_id LIKE {} OR title LIKE {} OR actress LIKE {} OR rapid_link LIKE {}) and length(rapid_link) > 0 and available is {}'.format(ss, ss, ss, ss, avail)
        condition = '(url_id LIKE {} OR title LIKE {} OR actress LIKE {} OR rapid_link LIKE {}) and available is {}'.format(ss, ss, ss, ss, avail)
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
        #u = up.upjav_hunter(db_name)
        u = up.javip_hunter(db_name)
         
        today = datetime.now().date()
        five_days_before = today - timedelta(days=3)
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
@app.route('/dl', methods=['GET'])
def dl():
    url = request.args.get('link')
    qq = rapidQQ(var.rapid_usr, var.rapid_passwd)
    ds = download_station(var.ds_ip, var.ds_port, var.ds_acct, var.ds_passwd)
     
    status_list = []
    if qq.is_link_valid(url) == False:
        status_list.append('URL not found')
    else: 
        ext_url = qq.extract_url(url)
        if ext_url == None:
            status_list.append('URL not found')
        else: 
            print("Ext URL={}".format(ext_url))
            status = ds.download(ext_url, var.ds_destination_path)
            status_list.append(status)
    return jsonify(results=status_list)
@app.route('/submit', methods=['POST'])
@nocache
def submit():
    my_json = request.json
    status_list = []
    if my_json == None:
        return jsonify(results=status_list)
    url_id = my_json.get('url_id')
    print("Get url_id from client '{}'".format(url_id))
    #u = up.upjav_hunter(db_name)
    u = up.javip_hunter(db_name)
    link = u.get_rapid_link_by_url_id(url_id)
    if link == None:
        return jsonify(results=status_list)
    qq = rapidQQ(var.rapid_usr, var.rapid_passwd)
    ds = download_station(var.ds_ip, var.ds_port, var.ds_acct, var.ds_passwd)
    for l in link[0][0].split(' '):
        if l == ' ' or l == '':
            continue
        print(l)
        if qq.is_link_valid(l) == False:
            status_list.append('URL not found')
            continue
        url = qq.extract_url(l)
        if url == None:
            status_list.append('URL not found')
            continue
        print("URL={}".format(url))
        status = ds.download(url, var.ds_destination_path)
        status_list.append(status)
    
    return jsonify(results=status_list)
    #return Response(body, 200, mimetype = "application/json")

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
 
@app.route('/javlib')
@nocache
def javlib():
    h = javlib_handler()
    m = h.search("ABP")
    dict_list = []
    if m != None:
        for ele in m:
            links = h.get_rapid_links(ele.rapid_links)
            dict_list.append({'title': ele.title, 'cover_link': ele.img_link, 'rapid_link': links}) 
    return render_template('javlib.html', packed_data=dict_list)

@app.route('/searchjavlib/<string:path>')
@nocache
def query_javlib(path):
    print("Current path = '{}'".format(path))
    
    h = javlib_handler()
    m = h.search(path)
    dict_list = []
    if m != None:
        for ele in m:
            links = h.get_rapid_links(ele.rapid_links)
            dict_list.append({'pid': ele.pid, 'title': ele.title, 'cover_link': ele.img_link, 'rapid_link': links}) 
    return render_template('javlib.html', packed_data=dict_list)

@app.route('/postjavlib', methods=['POST'])
@nocache
def postjavlib():
    global avail
    my_json = request.json
    body = ""
    if my_json != None:
        search_str = my_json.get('search_str')
        ary1 = {'url': search_str}
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
@werkzeug.serving.run_with_reloader
@nocache
def runServer():
    files = ['main.py']
    http_server = WSGIServer(('', 9487), app)
    http_server.serve_forever()
if __name__ == '__main__':
    runServer()
