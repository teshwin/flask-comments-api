from flask import Flask, request, jsonify, abort
from urllib.request import urlopen
from utils import *
from sys import exit
from os import makedirs, path
import json


# define data sources
data = dict()
sources = {
    'posts': 'https://jsonplaceholder.typicode.com/posts',
    'comments': 'https://jsonplaceholder.typicode.com/comments'
}

# retrieve data
for source, url in sources.items():
    try:
        response = urlopen(url)
        data[source] = json.loads(response.read())
        print(f'Loaded source: {source}')
    except Exception as e:
        print(f'Failed to retrieve data for source: {source}')
        exit(1)

# process data
data['posts'] = process_posts(data['posts'], data['comments'])
data['comments'] = process_comments(data['comments'])

# store data
try:
    if not path.exists('data/'):
        makedirs('data/')
    for e in data.keys():
        with open(f'data/{e}.json', 'w+') as f:
            json.dump(data[e], f)
        print(f'Stored {e}')
except:
    print('Failed to complete data storage')

# initialize Flask server
app = Flask(__name__)

@app.route('/<entity>/')
@app.route('/<entity>/<int:id>')
def get(entity, id=None):
    try:
        if id:
            # return by id
            id_key = f'{entity[:-1]}_id'
            return jsonify(list(filter(lambda x: x[id_key]==id, data[entity])))
        
        # create filters for args
        filter_funcs = [lambda x: x[k] == (int(v) if v.isdigit() else v) for k,v in request.args.items()]
        
        # filter records
        records = [r for r in data[entity] if all(f(r) for f in filter_funcs)]

        return jsonify(records)
    except Exception as e:
        abort(400)
