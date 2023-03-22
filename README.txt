This is the README file for A0218297U's and AXXXXXXXU's submission
Email(s): e0544333@u.nus.edu, 

== Python Version ==

I'm (We're) using Python Version <3.8.10 or replace version number> for
this assignment.

== General Notes about this assignment ==
overview

The program consist of indexing the corpus and enabling the user to search
through the processed corpus. The main method of comparison is utilizing the consine score
of each document with respect to the query. In addition, we convert each term in the query and documents
into a standardized vector space model. 

To explain the algorithm performed in the vector space model, we calculate the weights of each term in the
query with respect to a document that contains the same query term. 

The formula for weight calculation of the 1.query and 2. document is as such:

1. term frequency (tf) . inverse document frequency (idf)
2. term frequency (tf)
This follows the lnc.ltc rule.

Next, we calculate the normalization factor for the query and document, scaling each score by an amount ensures
that that all the terms in both query and document are in the same space.

Once all that is done, we calculate the cosine difference of a document with respect to a term in the query and
sum the results to form a predictive score of similiary between the query and the document.

Since we are only interested in the top K elements, we utilize a heap to retrieve the top K elements.

== Files included with this submission ==

index.py: Index the file and provide necessary information for the calculation of vector space model

search.py: Token and parse each query term to identify similar documents with respect to the query

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[X] I/We, A0000000X and A0000000X, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

We suggest that we should be graded as follows:

<Please fill in>

== References ==

