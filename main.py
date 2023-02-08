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
    request_url = "https://www.googleapis.com/customsearch/v1?key=/v1?q={QUERY}&key={API_KEY}&cx={ENG_ID}&num=10"
    resp = requests.get(request_url)
    raw_search_results = json.loads(resp.text)['items']
    results = []

    for i in raw_search_results:
        result = {
            'URL': i['link'],
            'Title': i['title'],
            'Summary': i['snippet']
        }
        results.append(result)

    return results


def feedbacks():
    res = retrieve_results()
    count = 0
    rel = 0
    for item in res:
        count += 1
        print("Result " + str(count))
        print("[")
        print(" URL: " + item['url'])
        print(" Title: " + item['title'])
        print(" Summary: " + item['summary'])
        print("]")

        feedback = input("Relevant(Y/N)? ")
        if feedback == 'Y' or feedback == 'y':
            item['relevant'] = True
            rel += 1
        if feedback == 'N' or feedback == 'n':
            item['relevant'] = False
        print("")

    return res, rel/10


def modify_query():
    pass


def main():
    handle_inputs()
    info, actual_precision = feedbacks()

    while actual_precision < DESIRED_PRECISION or actual_precision != 0:
        # Query expansion techniques
        print("Still below the desired precision of " + str(DESIRED_PRECISION))
        modify_query()
        info, actual_precision = feedbacks()
    print("Desired precision reached, done")


if __name__ == '__main__':
    main()
