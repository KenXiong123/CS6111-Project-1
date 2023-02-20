# CS6111-Project-1

## Team Members

Jingyue Qin(**jq2343**)

Ken Xiong(**kx2175**)

## Files list

1. README.pdf

2. proj1.tar.gz

3. transcript.txt

## Run the program

1. VM

   ```
   $ git clone https://github.com/KenXiong123/CS6111-Project-1.git
   $ cd CS6111-Project-1
   $ sudo apt-get install python3-pip
   $ pip install -r requirements.txt
   $ python3 main.py <google api key> <google engine id> <precision> <query>
   ```

   where:

   - <google api key> is your Google Custom Search JSON API Key 

   - <google engine id> is your Google Custom Search Engine ID 
   - <precision> is the target value for precision@10, a real number between 0 and 1
   - <query> is your query, a list of words in double quotes (e.g., “Milky Way”)

2. Local 

   ```
   $ cd project_path
   $ pip install -r requirements.txt
   $ python3 main.py <google api key> <google engine id> <precision> <query>
   ```

   where:

   - <google api key> is your Google Custom Search JSON API Key 

   - <google engine id> is your Google Custom Search Engine ID 
   - <precision> is the target value for precision@10, a real number between 0 and 1
   - <query> is your query, a list of words in double quotes (e.g., “Milky Way”)

## Internal design of the project

This is a Python project for an information retrieval system that exploits user-provided relevance feedback to improve the search results returned by Google.  Here is the description of our internal design:

1. The program begins by importing the necessary external libraries: json, sys, requests, numpy, and TfidfVectorizer from sklearn.feature_extraction.text.
2. The handle_inputs function fetches the necessary API key, engine ID, query, and desired precision rate from the command-line inputs.
3. The retrieve_results function uses the Google Custom Search API to retrieve the top ten search results based on the current query.
4. The relevance_feedback function displays the search results to the user and collects feedback on their relevance.
5. The improve_query function derives new words and adds them to the query to improve the precision rate. It does this by parsing the search results to build a collection of documents, calculating the tf-idf weightings of all the tokens, implementing Rocchio's algorithm to calculate a modified query vector, and sorting the modified query vector by tf-idf weights to derive a new query.
6. The Rocchio_algo function calculates the modified query vector by constructing the original query vector, calculating the mean of positive feedback from relevant documents, calculating the mean of negative feedback from non-relevant documents, and then calculating the modified query vector. 

External Libraries used are:

- json: to encode and decode JSON data.
- sys: to handle command-line arguments.
- requests: to make HTTP requests to Google Custom Search API.
- TfidfVectorizer: from scikit-learn, to compute tf-idf weights of the tokens in the collection of documents.
- numpy: to perform mathematical operations on arrays.

## Detailed description of the query-modification method

The query expansion technique that we adopt relies on Rocchio's algorithm and tf_idf weighting scheme. The modification process can be broken down into 4 steps outlined below:

1. Given the search results returned from the Google Custom Search Engine API, we parse the `snippet` field of the 10 results and build a collection of 10 documents.

   - Each row (document) corresponds to the `snippet` field of a search result.
   - Query is being appended as a part of the collection.

2. We utilized the `TfidfVectorizer` class from `sklearn` to calculate tf_idf weightings for all tokenized terms in the collection. We will obtain a (m x n) weighting matrix where m is 11 (10 documents and 1 query) and n is the number of terms in the collection. Each row represents a document that contains the tf_idf values for all the vocabularies in that respective document; terms that don't exist in the document will have a zero weighting.

3. We implemented the Rocchio's algorithm to generate a better representation of the existing query. Our implementation followed the formula in Chapter 9, "Relevance Feedback & Query Expansion" of the Manning, Raghavan, and Schütze "Introduction to Information Retrieval" textbook: 

   

   ![](https://p.ipic.vip/2p9r4q.png)

   - First, we construct the original query vector by simply extracting the last row of the tf_idf weighting matrix from Step 2
   - Then, we calculated the average positive feedback (relevant documents) and the average negative feedback (non-relevant documents). We parsed through the weighting matrix to distinguish the feedbacks and extract the respective rows to calculate the mean.
   - Last, we used a pre-defined set of alpha, beta, and gamma suggested from page 183 of Manning, Raghavan, and Schütze "Introduction to Information Retrieval", where α = 1, β = 0.75, and γ = 0.15. Given the constants, we plugged original query vector, positive feedback, and negative feedback into the equation to generate a modified query vector.

4. Based on the modified query vector from Step 3, we can sort the vector in descending order and find out the most two terms with the greatest weightings. These one or two words will be then appended to the original query. Notably, the order of the original query will not change and the term with greater weightings will be first added to the query from the new words generated by modified query vector.

## Google Custom Search Engine JSON API Key and Engine ID

**API key**: AIzaSyAp1Mlu_GczzUdNm34c8dLG0MC5v09gWXE

**Engine ID**: 02e16cfd8d0bbe48a



## Additional information

**Reference:** 

1. https://www.youtube.com/watch?v=a0xsnQRDhuM
2. http://www.cs.columbia.edu/~gravano/cs6111/proj1.html
3. https://nlp.stanford.edu/IR-book/ ch09, pg. 182

