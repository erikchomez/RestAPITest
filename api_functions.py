import csv

# when we go to zip KEYWORDS and a row in the tsv file, the order matters, which is why we use a list
KEYWORDS = ['productID', 'title', 'brandId', 'brandName', 'categoryId', 'categoryName']
# since the order of the stop words does not matter, we can use a set
STOPWORDS = {'for', 'with', 'and'}


def tsv_to_dict_app(path):
    tsv_file = open(path)
    read_tsv = csv.reader(tsv_file, delimiter='\t')

    data = tsv_to_dict(read_tsv)

    return data


def tsv_to_dict(tsv_file: 'tsv_file') -> list:
    """
    Converts a tsv file to a list of dictionaries
    :param tsv_file: tsv_file to be read
    :return: a list of dictionaries
    """
    list_of_tsv_dicts = [dict(zip(KEYWORDS, row)) for row in tsv_file]
    # print(list_of_tsv_dicts)
    return list_of_tsv_dicts


def autocomplete(data: 'list', request: dict) -> list:
    """
    Implements an autocomplete endpoint that can provide suggestions for product name, category,
    and brand given a prefix
    :param data: a list of dictionaries
    :param request: dictionary containing the request
    :return: a list of suggestions given a prefix
    """
    if request['type'] not in ['brand', 'name', 'category']:
        raise ValueError('Unsupported value for request type!')

    autocomplete_list = set()

    for i in data:
        if request['type'] == 'brand':
            if i['brandName'].startswith(request['prefix']):
                autocomplete_list.add(i['brandName'])

        elif request['type'] == 'name':
            if i['title'].startswith(request['prefix']):
                autocomplete_list.add(i['title'])

        elif request['type'] == 'category':
            if i['categoryName'].startswith(request['prefix']):
                autocomplete_list.add(i['categoryName'])

    return list(autocomplete_list)


def search(data: 'list', request: 'dict') -> list:
    """
    Provides a query endpoint that can provide search results for any field in the data with pagination.
    If the request contains multiple specified fields, the results will satisfy all conditions
    :param data: a list of dictionaries
    :param request: dictionary containing the request
    :return: a list of dictionaries containing the search results
    """
    search_list = []
    search_size = abs(request['pagination']['from'] - request['pagination']['size']) + 1

    for i in data:
        to_add = True
        for c in request['conditions']:
            if not i[c['type']] in c['values']:
                to_add = False

        if to_add:
            search_list.append(i)

        if len(search_list) == search_size:
            break

    return search_list


def keywords(data: list, request: dict) -> dict:
    """
    Provides an endpoint that provides keywords and their frequencies in product titles
    Keywords are whatever words appear in a title, the most_frequent function filters out the words in a
    title that are less than or equal to 1 character, and a few stop words that were defined at the top of
    this file.
    :param data: a list of dictionaries
    :param request: dictionary containing the request
    :return: a dictionary with a list as the only value which holds keywords and their frequency
    """
    keyword_frequencies = {'keywordFrequencies': []}

    for v in request['keywords']:
        keywords_dict = {v: 0}
        for i in data:
            if v in i:
                keywords_dict[i] +=1
        keyword_frequencies['keywordFrequencies'].append(keywords_dict)

    return keyword_frequencies


def most_frequent(data: list) -> dict:
    """
    Provides an endpoint that provides, at most, the top 10 frequent keywords
    Keywords must be greater than 1 character and must not be present in the stop words list
    defined at the top of this file.
    :param data:
    :return: a dictionary with a list as the only value which holds keywords and their frequency
    """
    keywords_dict = {}

    for i in data:
        for j in i['title'].split(' '):
            if len(j) > 1 and j.lower() not in STOPWORDS:
                keywords_dict[j] = keywords_dict.get(j, 0) + 1

    top_ten = {'mostFrequent': []}
    count = 0
    for k, v in sorted(keywords_dict.items(), key=lambda x: x[1], reverse=True):
        top_ten['mostFrequent'].append({k: v})
        count += 1

        if count == 10:
            break

    return top_ten


def main():
    tsv_file = open('data/sample_product_data.tsv')
    read_tsv = csv.reader(tsv_file, delimiter='\t')

    list_of_dicts = tsv_to_dict(read_tsv)

    auto_request = {'type': 'category', 'prefix': 'B'}

    search_request = {"conditions": [{"type": "brandName", "values": ["Brother", "Canon"]},
                                     {"type": "categoryName", "values": ["Printers & Scanners"]}],
                      "pagination": {"from": 1, "size": 3}
                      }

    keyword_request = {"keywords": ["toner", "ink"]}

    # print(autocomplete(list_of_dicts, auto_request))
    # print(search(list_of_dicts, search_request))
    # print(keywords(list_of_dicts, keyword_request))


if __name__ == '__main__':
    main()
