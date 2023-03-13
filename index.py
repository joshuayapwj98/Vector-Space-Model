#!/usr/bin/python3
import nltk
import sys
import getopt
import os
import pickle
import shutil
import sys

# improvements:
# use temp directory
# standardise index and positingmap

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

def buildDocIds(in_dir, out_file):
    inFiles = sorted([int(i) for i in os.listdir(in_dir)])
    with open(out_file, "wb") as out_file:
        pickle.dump(inFiles, out_file)

# assumes that input files are preprocessed
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
    
    buildDocIds(in_dir, "docIds.txt")
    dictionary = {}
    index = {}

    inFiles = sorted(os.listdir(in_dir), key = lambda x: int(x))

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

        contents = contents.lower() # case folding
        sentences = nltk.tokenize.sent_tokenize(contents)
        
        words = [] 
        for sentence in sentences:
            words.extend(nltk.tokenize.word_tokenize(sentence)) 

        stemmed_words = [stemmer.stem(word) for word in words]
        processed_words = ' '.join(stemmed_words)

         # Write processed contents to tmp directory
        with open(os.path.join(TMP_DIR, file_name), 'w') as f:
            f.write(processed_words)
    
    in_dir = TMP_DIR # change the input directory to the processed documents folder 
    inFiles = sorted(os.listdir(in_dir), key = lambda x: int(x))

    for inFile in inFiles:
        with open(os.path.join(in_dir, inFile), "r", encoding="utf-8") as f:
            fileSet = set()

            for line in f:
                words = line.split()
                for word in words:
                    fileSet.add(word)

            for word in fileSet:
                if word not in dictionary.keys():
                    dictionary[word] = len(dictionary.keys())
                    index[dictionary[word]] = []
                index[dictionary[word]].append(int(inFile))

    startIdx = 0

    with open(out_postings, "wb") as postingsFile:
        for word in dictionary:
            # pointer is in the form [start index, size of pickle-serialised linkedlist in bytes]
            dictionary[word] = [startIdx, postingsFile.write(pickle.dumps(index[dictionary[word]]))]
            print(word, dictionary[word][0], dictionary[word][1])
            startIdx += dictionary[word][1]

    with open(out_dict, "wb") as dictFile:
        pickle.dump(dictionary, dictFile)


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
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

# increaseRecursionLimit()
build_index(input_directory, output_file_dictionary, output_file_postings)