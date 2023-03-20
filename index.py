#!/usr/bin/python3
import nltk
import sys
import getopt
import os
import pickle
import shutil
import sys
import collections
import math

# improvements:
# use temp directory
# standardise index and positingmap


def usage():
    print("usage: " +
          sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")


def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('indexing...')
    # This is an empty method
    # Pls implement your code in below

    if not os.path.exists(in_dir):
        print("ERROR: in dir not exist")
        sys.exit(2)

    inFiles = sorted(os.listdir(in_dir), key=lambda x: int(x))

    # pre-process the documents, first by tokenising the sentences,
    # then words, then apply porter stemming and then finally writitng the result
    # of the procesed file into a dictery consisting of all the processed documents.

    TMP_DIR = "processed"
    stemmer = nltk.stem.PorterStemmer()
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    for file_name in inFiles:

        with open(os.path.join(in_dir, file_name), 'r') as f:
            contents = f.read()

        contents = contents.lower()  # case folding
        sentences = nltk.tokenize.sent_tokenize(contents)

        words = []
        for sentence in sentences:
            words.extend(nltk.tokenize.word_tokenize(sentence))

        stemmed_words = [stemmer.stem(word) for word in words]
        processed_words = ' '.join(stemmed_words)

        # Write processed contents to tmp directory
        with open(os.path.join(TMP_DIR, file_name), 'w') as f:
            f.write(processed_words)

    in_dir = TMP_DIR  # change the input directory to the processed documents folder
    inFiles = sorted(os.listdir(in_dir), key=lambda x: int(x))
    index = collections.defaultdict(lambda: [])
    documentLength = collections.defaultdict(lambda: 0)
    documentWeight = collections.defaultdict(lambda: 0)

    for inFile in inFiles:
        with open(os.path.join(in_dir, inFile), "r", encoding="utf-8") as f:
            termFreq = collections.defaultdict(lambda: 0)

            for line in f:
                words = line.split()
                for word in words:
                    termFreq[word] += 1
                    documentLength[int(inFile)] += 1
            
            square_sum = 0
            for word in termFreq:
                index[word].append([int(inFile), termFreq[word]])
                square_sum += termFreq[word] * termFreq[word]

            # add the normalization factor for computation in search
            documentWeight[int(inFile)] = math.sqrt(square_sum)

    startIdx = 0

    with open(out_postings, "wb") as postingsFile:
        for word in index:
            # pointer is in the form [start index, size of pickle-serialised linkedlist in bytes]
            pointer = [startIdx, postingsFile.write(pickle.dumps(index[word]))]

            # value is in the form of [document frequency, pointer]
            documentFrequency = len(index[word])
            index[word] = [documentFrequency, pointer]

            # print(word, index[word][1][0], index[word][1][1])
            startIdx += index[word][1][1]

    with open(out_dict, "wb") as dictFile:
        pickle.dump(dict(index), dictFile)

    with open("docData.txt", "wb") as docData:
        pickle.dump(dict(documentWeight), docData)

    # cleanup
    shutil.rmtree(TMP_DIR)
    print("done")

# # pickle recursion exceeds limit otherwise
# # code taken from https://stackoverflow.com/questions/2134706/hitting-maximum-recursion-depth-using-pickle-cpickle
# def increaseRecursionLimit():
#     max_rec = 0x100000

#     # May segfault without this line. 0x100 is a guess at the size of each stack frame.
#     resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
#     sys.setrecursionlimit(max_rec)


input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i':  # input directory
        input_directory = a
    elif o == '-d':  # dictionary file
        output_file_dictionary = a
    elif o == '-p':  # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

# increaseRecursionLimit()
build_index(input_directory, output_file_dictionary, output_file_postings)
