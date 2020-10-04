from flask import Flask, request, jsonify, render_template, flash, redirect, url_for

import api_functions as api
import os
import json

# folder containing the data
DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DATA')

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['DATA_FOLDER'] = DATA_FOLDER

FILE = api.tsv_to_dict_app(os.path.join(app.config['DATA_FOLDER'], 'sample_product_data.tsv'))


@app.route('/')
def index():
    # renders the web page
    return render_template('index.html')


@app.route('/api/products/all', methods=['GET'])
def api_all():
    """
    Returns the file containing all the products in a JSON object
    :return:
    """
    return jsonify(FILE)


def auto_complete_query_checker(query_params: dict) -> bool:
    """
    Helper function that returns a bool determining if the query parameters are formatted properly.
    :param query_params: dictionary containing the query parameters
    :return: True or False depending on the formatting
    """
    query_keys = list(query_params.keys())

    # type and prefix must appear in the list of query keys. If even one is not present, the query was not
    # formatted properly
    if 'type' not in query_keys or 'prefix' not in query_keys:
        return False

    # if the value for type is not in the given list, then it was not formatted properly
    if query_params['type'] not in ['name', 'brand', 'category']:
        return False

    # if it passes the last two checks, then the query was formatted correctly
    return True


@app.route('/api/products/autocomplete', methods=['GET'])
def auto_complete():
    query_params = request.args.to_dict(flat=True)

    if query_params:
        if auto_complete_query_checker(FILE, query_params):
            l1 = api.autocomplete(query_params)
            return jsonify(l1)
        else:
            flash('Query parameters formatted incorrectly.')
            return render_template('index.html')

    else:
        flash('Query parameters were empty. Please specify parameters in the following format:'
              '?type={}&prefix={}')

        return render_template('index.html')


def search_query_checker(query_params: dict) -> bool:
    request_keys = set(query_params.keys())
    # makes sure that the length of the keys is 2, anything more is wrong
    if len(request_keys) != 2:
        return False

    # conditions and pagination must be in the keys, otherwise it is wrong
    if 'conditions' not in request_keys and 'pagination' not in request_keys:
        return False

    # checks to make sure from is an int
    if type(query_params['pagination']['from']) is not int:
        return False

    # checks to make sure size is an int
    if type(query_params['pagination']['size']) is not int:
        return False

    # checks to make sure the from pagination is valid
    if query_params['pagination']['from'] < 1:
        return False

    # makes sure the size is greater than the initial from
    if query_params['pagination']['size'] < query_params['pagination']['from']:
        return False

    return True


@app.route('/api/products/search', methods=['GET'])
def search():
    search_request = {"conditions": [{"type": "brandName", "values": ["Brother", "Canon"]},
                                     {"type": "categoryName", "values": ["Printers & Scanners"]}],
                      "pagination": {"from": 1, "size": 3}
                      }
    query_params = request.args.to_dict(flat=True)

    if not query_params:
        if search_query_checker(search_request):
            l1 = api.search(FILE, search_request)

            return jsonify(l1)
        else:
            flash('Query parameters formatted incorrectly.')
            return render_template('index.html')
    else:
        flash('Query parameters invalid.')
        return render_template('index.html')


def keywords_query_checker(query_params: dict) -> bool:
    """
    Helper function that returns a bool determining if the query parameters are formatted properly.
    :param query_params: dictionary containing the query parameters
    :return: True or False depending on the formatting
    """
    request_keys = set(query_params.keys())

    # the length of the request keys must be 1 since we are only looking for keywords
    if len(request_keys) != 1:
        return False
    # however, if the length is 1, we want keywords to be the only value
    if 'keywords' not in request_keys:
        return False

    # if it passes the last two checks, then the query was formatted correctly
    return True


@app.route('/api/products/keywords', methods=['GET'])
def keywords():
    query_params = request.args.to_dict(flat=False)

    if query_params:
        if keywords_query_checker(query_params):
            l1 = api.keywords(FILE, query_params)
            return jsonify(l1)
        else:
            flash('Query parameters formatted incorrectly.')
            return render_template('index.html')
    else:
        flash('Query parameters were empty. Please specify parameters in the following format:'
              '?keywords={}')

        return render_template('index.html')


@app.route('/api/products/mostfrequent', methods=['GET'])
def custom():
    l1 = api.most_frequent(FILE)

    return jsonify(l1)


if __name__ == '__main__':
    app.run(host='localhost', port='8088', debug=True)