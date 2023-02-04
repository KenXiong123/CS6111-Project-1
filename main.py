import json
import sys
import requests

API_KEY = ''
ENG_ID = ''
DESIRED_PRECISION = 0
QUERY = ''


def handle_inputs():
    parameters = sys.argv
    global API_KEY, ENG_ID, DESIRED_PRECISION, QUERY
    API_KEY, ENG_ID, DESIRED_PRECISION, QUERY = parameters[1], parameters[2], parameters[3], parameters[4]


def retrieve_results():
    request_url = "https://www.googleapis.com/customsearch/v1?key=" + API_KEY + "&cx=" + ENG_ID + "&q=" + QUERY
    resp = requests.get(request_url)
    raw_search_results = json.loads(resp.text)['items']
    results = []

    for i in range(0, 10):
        result = {
            'URL': raw_search_results[i]['link'],
            'Title': raw_search_results[i]['title'],
            'Summary': raw_search_results[i]['snippet']
        }
        results.append(result)

    return results


# def collect_feedbacks():
#
# def modify_query():

def main():
    handle_inputs()
    results = retrieve_results()
    # actual_precision = collect_feedbacks(results)
    #
    # while actual_precision < DESIRED_PRECISION or actual_precision != 0:
    #     # Query expansion techniques
    #     modify_query()
    #     results = retrieve_results()
    #     actual_precision = collect_feedbacks(results)


if __name__ == '__main__':
    main()
