from flask import Flask, request, jsonify, render_template

import api_functions as api
import os
import json
import urllib
import requests

DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DATA')

app = Flask(__name__)
app.config['DATA_FOLDER'] = DATA_FOLDER

FILE = api.tsv_to_dict_app(os.path.join(app.config['DATA_FOLDER'], 'sample_product_data.tsv'))


@app.route('/')
def index():
    # renders the web page
    return render_template('index.html')


@app.route('/api/products/all', methods=['GET'])
def api_all():
    return jsonify(FILE)


@app.route('/api/products/autocomplete', methods=['GET', 'POST'])
def auto_complete():
    query_params = request.args.to_dict(flat=True)
    # print(query_params)
    l1 = api.autocomplete(FILE, query_params)
    return jsonify(l1)


@app.route('/api/products/search', methods=['GET'])
def search():
    # search_request = {"conditions": [{"type": "brandName", "values": ["Brother", "Canon"]},
    #                                  {"type": "categoryName", "values": ["Printers & Scanners"]}],
    #                   "pagination": {"from": 1, "size": 3}
    #                   }
    #
    # l1 = api.search(FILE, search_request)
    #
    # return jsonify(l1)

    response = requests.post('http://0.0.0.0:8088/search', json={'key': 'value'})
    response.request.headers['Content-Type']

    print(response.request.url)
    print(response,request.body)


@app.route('/api/products/keywords', methods=['GET'])
def keywords():
    query_params = request.args.to_dict(flat=False)
    l1 = api.keywords(FILE, query_params)

    return jsonify(l1)


@app.route('/api/products/custom', methods=['GET'])
def custom():
    l1 = api.most_frequent(FILE)

    return jsonify(l1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8088', debug=True)