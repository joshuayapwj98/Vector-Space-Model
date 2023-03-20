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
        _document_weights = pickle.load(doclen_file)
        N = len(_document_weights)

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
                result = process_query(query, dictionary, postings_file, _document_weights)
                output_builder = ', '.join(map(str, result))
                results_file.write(output_builder + '\n')


# ====================================================================
# ====================== RANKING PROCESSING ==========================
# ====================================================================

def get_query_term_weight(query_term, termIndex):
    return calculate_term_frequency(query_term, termIndex) * calculate_inverse_document_frequency(query_term, termIndex)

def get_document_term_weight(document_term):
    return 1 + math.log(document_term, 10)

def calculate_term_frequency(term, termIndex):
    return 1 + math.log(termIndex[term], 10)

def calculate_inverse_document_frequency(term, termIndex):
    global N
    return math.log(N/termIndex[term])

def get_top_K_components(scores_dic, K):
    result = []
    score_tuples = [(-score, doc_id) for doc_id, score in scores_dic.items()]
    heapq.heapify(score_tuples)
    top_K = heapq.nlargest(K, score_tuples)
    for tuple in top_K:
        result.append(tuple[1])

    return result

# ==============================================================
# ====================== QUERY PROCESSING ======================
# ==============================================================

def process_query(query, dictionary, postings_file, _document_weights):
    global N
    global K
    queryIndex = collections.defaultdict(lambda: 0)
    query = query.strip().split()
    score_dic = collections.defaultdict(lambda: 0)

    for word in query:
        queryIndex[word] += 1

    for term in queryIndex:
        # for each word in the query, get the tf.idf
        query_term_weight = get_query_term_weight(term, queryIndex)
        postingList = single_word_query(term, dictionary, postings_file)

        # [documentId, frequency]
        for frequencyPair in postingList:
            document_term_weight = get_document_term_weight(frequencyPair[1])
            # TODO: clarify here
            document_normalized_weight = (document_term_weight / _document_weights[frequencyPair[0]])
            query_normalized_weight = (query_term_weight / math.sqrt(query_term_weight * query_term_weight))
            score_dic[frequencyPair[0]] += document_normalized_weight * query_normalized_weight
    return get_top_K_components(score_dic, K)

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
    stemmer = nltk.stem.PorterStemmer()
    word = stemmer.stem(word.lower())  # case folding and stemming

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
