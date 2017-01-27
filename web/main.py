# web interface
import sys
from flask import Flask, render_template, abort
from gevent.wsgi import WSGIServer
import json
import upjav_hunter as up

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

def search_db(search_string):
    try:
        u = up.upjav_hunter("tmp5.db")
        ss = '"%{}%"'.format(search_string)
        condition = 'pid LIKE {} OR title LIKE {} OR actress LIKE {} OR rapid_link LIKE {}'.format(ss, ss, ss, ss)
        my_dict_list = u.query_data(condition)
        print("{} Matched".format(len(my_dict_list)))
        return my_dict_list
    except Exception as e:
        print("Error: {}".format(e))

@app.route('/')
def home():
    my_dict_list = search_db("RION")
    return render_template('index.html', packed_data=my_dict_list)
@app.route('/<path:path>')
def query(path):
    my_dict_list = search_db(path)
    return render_template('index.html', packed_data=my_dict_list)

if __name__ == '__main__':
    http_server = WSGIServer(('', 9487), app)
    http_server.serve_forever()
