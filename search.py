#!/usr/bin/python3
import nltk
import sys
from nltk.stem.porter import PorterStemmer
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

    with open(f'{queries_file}', "r") as queries_file,\
        open(f'{postings_file}', 'r') as postings_file,\
        open(f'{results_file}', "w") as results_file:
    
        queries_text = queries_file.read()
        queries = queries_text.split('\n')

        # Process each query and write results to the results file
        for i, query in enumerate(queries):
            if query == '':
                # Empty line in queries.txt
                results_file.write("\n")
            else:
                post_fix = get_postfix(query)

# ====================================================================
# ====================== RANKING PROCESSING ==========================
# ====================================================================

def calculate_score(query_term_arr, term_dictionary, postings_list):
    global N
    Scores, Length = [0] * N
    documents = []
    for query_term in query_term_arr:
        qt_weight = get_query_term_weight(query_term)
        term_postings_list = get_postings_list(query_term, term_dictionary, postings_list)
        for documentId in term_postings_list:
            # Track which document is used for normalization
            documents.append(documentId)
            Scores[documentId] += get_document_term_weight(query_term) * qt_weight
    
    for documentId in documents:
        Scores[documentId] = Scores[documentId] / Length[documentId]
    return get_top_K_components(Scores)

        

def get_query_term_weight(query_term):
    # TODO
    return

def get_document_term_weight(query_term):
    # TODO
    return

def calculate_term_frequency(term, term_dictionary):
    # TODO
    return

def calculate_inverse_document_frequency(term, term_dictionary):
    # TODO
    return

def get_top_K_components(Scores):
    # TODO
    return
# ==============================================================
# ====================== QUERY PROCESSING ======================
# ==============================================================

def process_query(tokens, term_dictionary, postings_file):
    stack = []
    for token in tokens:
        if token not in OPS_DICTIONARY:
            # Regular string term
            stack.append(token)
        else:
            # Pop the next term in the stack and retrieve the postings_list 
            left_operand = posting_list_type_check(stack.pop(), postings_file)
            intermediate_result = []
            if token == 'NOT':
                # TODO: Perform 'NOT' operation
                return
            elif token == 'AND':
                # Pop the next term in the stack and retrieve the postings_list 
                right_operand = posting_list_type_check(stack.pop(), term_dictionary, postings_file)
                operands = [left_operand, right_operand]
                # TODO: Perform 'AND' operation on the operands and gets the postings_list
                return

            elif token == 'OR':
                # Pop the next term in the stack and retrieve the postings_list 
                right_operand = posting_list_type_check(stack.pop(), term_dictionary, postings_file)
                operands = [left_operand, right_operand]
                # TODO: Perform 'OR' operation on the operands and gets the postings_list
                return
            
            # Append the result to the stack
            stack.append(intermediate_result)

    if len(stack) > 0:
        query_result = stack.pop()
        # Edge case: If there is only 1 querable term, retrieve the individual postings_list and return
        if type(query_result) == str:
            query_result = get_postings_list(query_result, term_dictionary, postings_file)
        return query_result
    else:
        # TODO: 
        # Edge case: No results for the query
        return []

def posting_list_type_check(operand, term_dictionary, postings_file):
    """
    Returns the postings_list of the operand if it is a string term.
    """
    if type(operand) != list:
        # Get the operand's postings_list
        operand = get_postings_list(operand, term_dictionary, postings_file)
    return operand

def get_postfix(infix):
    """
    Converts an infix expression to Reverse Polish Notation using the Shunting Yard algorithm.
    """
    # Initialize stack and queue
    operators = []
    postfix = []
    global OPS_DICTIONARY

    # Split the infix expression into tokens
    tokens = tokenize(infix)

    for token in tokens:
        if token in OPS_DICTIONARY:
            # Check if the top operator is in the ops_dict and the
            # precedence of it is greater than the current token
            while operators and operators[-1] in OPS_DICTIONARY and \
                  OPS_DICTIONARY[operators[-1]] > OPS_DICTIONARY[token]:
                # Append the operator into the postfix list
                # Pop the operator from the operators stack
                postfix.append(operators.pop())
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators[-1] != "(":
                postfix.append(operators.pop())
            operators.pop()
            if len(operators) == 0:
                # Incomplete parenthesis, exit the program
                exit()
        else:
            postfix.append(stemmer.stem(token.lower()))
    
    while operators:
        postfix.append(operators.pop())
    
    postfix = [token for token in postfix if token not in ['(', ')']]
    return postfix
   

def tokenize(query):
    """
    Tokenizes a query into individual terms
    """
    tokens = []
    curr = ''

    for char in query:
        if char == '(' or char == ')':
            if curr:
                tokens.append(curr)
                curr = ''
            tokens.append(char)
        elif char == ' ':
            if curr:
                tokens.append(curr)
                curr = ''
        else:
            curr += char

    if curr:
        tokens.append(curr)

    return tokens

# ===================================================================
# ====================== ACCESS INDEXING FILES ======================
# ===================================================================

def get_postings_list(term, term_dictionary, postings_file):
    """
    Returns the postings list for the given term.
    """
    if term not in term_dictionary:
        return []
    
    file_ptr_pos = term_dictionary.get(term)[1]

    # Move the file pointer to the start of the array
    postings_file.seek(int(file_ptr_pos))

    # Read the bytes from the file until the end of the line
    line_bytes = postings_file.readline()

    # Remove the newline character from the end of the line
    line_bytes = line_bytes.rstrip('\n')
    
    # Convert the string back to a list
    postings_list = eval(line_bytes)

    return postings_list


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
