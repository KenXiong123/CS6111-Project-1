import json
import sys
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

API_KEY = ''
ENG_ID = ''
DESIRED_PRECISION = 0
QUERY = ''


def handle_inputs():
    """
    Fetch API key, engine ID, query, and desired precision rate from command line inputs
    :return: void
    """
    parameters = sys.argv
    global API_KEY, ENG_ID, DESIRED_PRECISION, QUERY
    API_KEY, ENG_ID, DESIRED_PRECISION, QUERY = parameters[1], parameters[2], float(parameters[3]), parameters[4]


def retrieve_results():
    """
    Invoke google search engine API to retrieve top 10 results based on the current query
    :return: An array of dicts; each dict represents one search result
    """
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


def relevance_feedbacks():
    """
    Collect user feedbacks on relevance
    :return: Search result array and overall actual precision rate
    """
    res = retrieve_results()
    count = 0
    rel = 0
    print("Parameters:")
    print("Client key = " + API_KEY)
    print("Engine key = " + ENG_ID)
    print("Query      = " + QUERY)
    print("Precision  = " + str(DESIRED_PRECISION))
    print("Google Search Results:")
    print("======================")
    for item in res:
        count += 1
        print("Result " + str(count))
        print("[")
        print(" URL: " + item['URL'])
        print(" Title: " + item['Title'])
        print(" Summary: " + item['Summary'])
        print("]")

        feedback = input("Relevant(Y/N)? ")
        if feedback.upper() == 'Y':
            item['relevant'] = True
            rel += 1
        if feedback.upper() == 'N':
            item['relevant'] = False
        print("")

    return res, rel / 10


def improve_query(res):
    """
    Derive new words and add them to the query to improve precision rate
    1. Parse search results to build a collection of documents (e.g. analyze "snippet" field of each result)
    2. Calculate tf_idf weightings of all the tokens
    3. Implement Rocchio's algo to calculate modified query vector
    4. Sort the modified query vector by tf-idf weights and derive new query
    :return: void
    """
    # Step 1
    global QUERY
    original_query = QUERY.split()
    collection = []
    for result in res:
        collection.append(result['Summary'])
    collection.extend(original_query)

    # Step 2
    vectorizer = TfidfVectorizer()
    tf_idf = vectorizer.fit_transform(collection)

    # Step 3
    modified_query = rocchio_algo(res, tf_idf)

    # Step 4
    modified_query_sorted = np.sort(modified_query)[::-1]
    tokens = vectorizer.get_feature_names_out()
    modified_query_weights = {}
    for i in range(len(tokens)):
        modified_query_weights[modified_query[i]] = tokens[i]

    max_new_words = 2
    new_query = original_query
    new_words = []
    for j in range(len(modified_query_sorted)):
        word = modified_query_weights.get(modified_query_sorted[j])
        if word in original_query:
            continue
        else:
            new_query.append(word)
            new_words.append(word)
            max_new_words -= 1
        if max_new_words == 0:
            break
    QUERY = " ".join(str(word) for word in new_query)

    return new_words


def rocchio_algo(results, tf_idf):
    """
    1. Construct the original query vector
    2. Calculate the mean of positive feedback from relevant docs
    3. Calculate the mean of negative feedback from non-relevant docs
    4. Calcualte the modified query vector
    :param results: search result set
    :param tf_idf: weighting scheme
    :return: modified query vector
    """

    alpha, gamma, beta = 1, 0.75, 0.15

    # Step 1
    original_q_vec = np.array(tf_idf.toarray()[-1])

    # Step 2 & Step 3
    pos_num = 0
    neg_num = 0
    pos_sum = np.zeros(len(original_q_vec))
    neg_sum = np.zeros(len(original_q_vec))
    for index in range(len(results)):
        if results[index]['relevant']:
            pos_num += 1
            pos_sum += tf_idf.toarray()[index]
        else:
            neg_num += 1
            neg_sum += tf_idf.toarray()[index]
    pos_feedback = pos_sum / pos_num
    neg_feedback = neg_sum / neg_num

    # Step 4
    modified_q_vec = alpha * original_q_vec + beta * pos_feedback - gamma * neg_feedback

    return modified_q_vec


def print_summary(actual_precision, new_words):
    print("======================")
    print("FEEDBACK SUMMARY")
    print("Query " + QUERY)
    print("Precision " + str(actual_precision))
    if actual_precision < DESIRED_PRECISION:
        print("Still below the desired precision of " + str(DESIRED_PRECISION))
        print("Indexing results ....")
        print("Augmenting by " + " ".join(str(word) for word in new_words))
    else:
        print("Desired precision reached, done")


def main():
    handle_inputs()
    res, actual_precision = relevance_feedbacks()
    if len(res) < 10:
        print('Fewer than 10 results in the first iteration. Please search again!')
        quit()
    if actual_precision == 0:
        print("Below desired precision, but can no longer augment the query")
        quit()
    new_words = []
    while actual_precision < DESIRED_PRECISION:
        # Query expansion techniques
        new_words = improve_query(res)
        print_summary(actual_precision, new_words)
        res, actual_precision = relevance_feedbacks()
    print_summary(actual_precision, new_words)


if __name__ == '__main__':
    main()
