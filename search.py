#!/usr/bin/python3
import nltk
import sys
import getopt
import collections
import math
import pickle


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

    with open(dict_file, "rb") as dict_file:
        # <word in string form, [document frequency, [start byte address, size in bytes]]>>
        dictionary = pickle.load(dict_file)

    with open("docData.txt", "rb") as doclen_file:
        documentLength = pickle.load(doclen_file)

    # Process the queries and output
    scores = collections.defaultdict(lambda: 0)
    with open(queries_file, "r") as query_file, open(results_file, "w+") as out_file:
        for queryLine in query_file:
            queryIndex = collections.defaultdict(lambda: 0)

            query = queryLine.strip().split()
            for word in query:
                queryIndex[word] += 1

            for word in queryIndex:
                # get query tfidf
                queryTf = 1 + math.log(queryIndex[word], 10)
                queryIdf = math.log(len(documentLength)/dictionary[word][0])
                queryWeight = queryTf * queryIdf

                postingList = single_word_query(
                    word, dictionary, postings_file)

                # for each document in posting list, get tf and multiply by queryWeight
                for freqPair in postingList:
                    docTf = 1 + math.log(freqPair[1], 10)
                    scores[freqPair[0]] += docTf * queryWeight

            # normalise
            for docId in scores:
                scores[docId] /= documentLength[docId]

            # chuck scores into a heap and print out the top 5


def single_word_query(word, dictionary, postings_file):
    """
    Given a word in string and dictoanay and a file of documents postings 
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
