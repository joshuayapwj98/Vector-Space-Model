#!/usr/bin/python3
import nltk
import sys
import math
import collections
import pickle
from nltk.stem.porter import PorterStemmer
import getopt
import collections
import math
import pickle
import heapq

stemmer = PorterStemmer()

# Global variable(s)
N = 0
K = 10

def usage():
    print("usage: " +
          sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")


def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')
    # This is an empty method
    # Pls implement your code in below

    global N
    
    with open(dict_file, "rb") as dict_file:
        # <word in string form, [document frequency, [start byte address, size in bytes]]>>
        dictionary = pickle.load(dict_file)

    with open("docData.txt", "rb") as doclen_file:
        document_term_weights_dict = pickle.load(doclen_file)
        N = len(document_term_weights_dict)

    with open(f'{queries_file}', "r") as queries_file,\
        open(f'{results_file}', "w") as results_file:
    
        queries_text = queries_file.read()
        queries = queries_text.split('\n')

        # Process each query and write results to the results file
        for i, query in enumerate(queries):
            if query == '':
                # Empty line in queries.txt
                results_file.write("\n")
            else:
                stemmed_query = tokenize_query(query)
                result = process_query(stemmed_query, dictionary, postings_file, document_term_weights_dict)
                output_builder = ', '.join(map(str, result))
                results_file.write(output_builder + '\n')


# ====================================================================
# ====================== RANKING PROCESSING ==========================
# ====================================================================

def get_query_term_weight(query_term, termIndex, postings_list_len):
    global N
    if postings_list_len == 0:
        return 0
    return (1 + math.log(termIndex[query_term], 10)) * math.log(N/postings_list_len)

def get_document_term_weight(document_term_frequency):
    return 1 + math.log(document_term_frequency, 10)
    
def get_top_K_components(scores_dic, K):
    result = []
    score_tuples = [(-score, doc_id) for doc_id, score in scores_dic.items()]
    
    heapq.heapify(score_tuples)
    for i in range(K):
        tuple_result = heapq.heappop(score_tuples)
        result.append(tuple_result[1])

    return result

# ==============================================================
# ====================== QUERY PROCESSING ======================
# ==============================================================

def process_query(query, dictionary, postings_file, document_term_weights_dict):
    global K
    queryIndex = collections.defaultdict(lambda: 0)
    query_weight_dict = collections.defaultdict(lambda: 0)
    
    score_dict = collections.defaultdict(lambda: 0)

    for word in query:
        queryIndex[word] += 1

    square_val_list = []
    # Get all the sum of (query weight)^2
    for word in queryIndex:
        postingList = single_word_query(word, dictionary, postings_file)
        query_term_weight = get_query_term_weight(word, queryIndex, len(postingList))
        query_weight_dict[word] = query_term_weight
        square_val_list.append(query_term_weight ** 2)
    
    square_val_list.sort()
    square_sum = sum(square_val_list)

    # Get the query normalization factor 
    query_normalization_factor = math.sqrt(square_sum)

    for term in queryIndex:
        # get normalised query vector item
        postingList = single_word_query(term, dictionary, postings_file)
        query_term_weight = query_weight_dict[term]
        query_term_weight /= query_normalization_factor

        # get normalised document vector item, then add score
        # [documentId, frequency]
        for frequencyPair in postingList:
            currScore = document_term_weights_dict[frequencyPair[0]][term] * query_term_weight
            score_dict[frequencyPair[0]] += currScore

    return get_top_K_components(score_dict, K)

def tokenize_query(query):
    query = query.strip().split()
    terms = []
    stemmer = nltk.stem.PorterStemmer()

    for term in query:
        stemmed = stemmer.stem(term.lower())
        terms.append(stemmed)
    
    return terms

# ===================================================================
# ====================== ACCESS INDEXING FILES ======================
# ===================================================================

def single_word_query(word, dictionary, postings_file):
    """
    Given a word in string, dictionary and a file of documents postings 
    it returns a list with all the documents_posting found in the dictonary. 
    Params: word: string, dictionary : a dictonray object loaded into memory, 
            postings_file: string path to the file of postings_file 
    Returns: a list object consisting of all the documents posting of the words 
    in the dictonary. 
    """

    # -1 means that the word doesn't exist
    [_, [start, sz]] = dictionary.get(word, [-1, [-1, -1]])

    if start != -1:
        with open(postings_file, "rb") as post_file:
            post_file.seek(start)
            return pickle.loads(post_file.read(sz))

    return []

dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None:
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
