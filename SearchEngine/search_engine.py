# -------------------------------------------------------------------------
# AUTHOR: Joshua Furman
# FILENAME: search_engine.py
# SPECIFICATION: Given a query, read a .csv file and output the accuract of a proposed search engine
# FOR: CS 4250- Assignment #1
# TIME SPENT: 2 hrs
# -----------------------------------------------------------*/

# IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to
# work here only with standard arrays

# importing some Python libraries
import csv
import math

documents = []
labels = []

# reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i > 0:  # skipping the header
            documents.append(row[0])
            labels.append(row[1])

# Conduct stopword removal.
# --> add your Python code here
stopWords = {'I', 'and', 'She', 'They', 'her', 'their'}
counter = 0
for doc in documents:
    doc = doc.split()
    for word in doc:
        if word in stopWords:
            doc.remove(word)
    documents[counter] = doc
    counter += 1

# at this point documents is a multidimentional list with stopwords removed.
# EX: [['love', 'cats', 'cats'], ['loves', 'dog'], ['love', 'dogs', 'cats']]

# Conduct stemming.
# --> add your Python code here
stemming = {
    "cats": "cat",
    "dogs": "dog",
    "loves": "love",
}
newDocs = []

# iterate through the new documents and change all dictionary keys to their value pairs
for document in documents:
    newDoc = [stemming.get(word, word) for word in document]
    newDocs.append(newDoc)

# Identify the index terms.
# --> add your Python code here
terms = []
for doc in newDocs:
    for item in doc:
        terms.append(item)

# use a set to get rid of duplicates
terms = set(terms)
terms = list(terms)
# Build the tf-idf term weights matrix.
# --> add your Python code here
tfValues = []

# calculate a list of tf values
j = 0
# loop 3 times, index is the tf value were trying to find like dog, love, and cat respectively
while j < len(terms):
    index = terms[j]
    j += 1
    for doc in newDocs:
        occurances = 0
        for term in doc:
            if term == index:
                occurances += 1
        tf = occurances / len(doc)
        tfValues.append(tf)

idfValues = []
# calculate idf values
x = 0
while x < len(terms):
    idf = 0
    index = terms[x]
    x += 1
    occurances = 0
    for doc in newDocs:
        if index in doc:
            occurances += 1
    idf = math.log10(3 / occurances)
    idfValues.append(idf)

# Calculate the document scores (ranking) using document weigths (tf-idf) calculated before and query weights (binary
# - have or not the term). --> add your Python code here
docScores = []
tfidfScores = []
dex = 0
while dex < len(idfValues):
    currentIdf = idfValues[dex]
    tfidf_group = []
    for i in range(3 * dex, 3 * (dex + 1)):
        tfidf = currentIdf * tfValues[i]
        tfidf = round(tfidf, 4)
        tfidf_group.append(tfidf)
    tfidfScores.append(tfidf_group)
    dex += 1

print("TF-IDF scores are as follows from above: ")

# here is where I actually calcuate doc scores
doc1Score = sum(section[0] for section in tfidfScores)
doc2Score = sum(section[1] for section in tfidfScores)
doc3Score = sum(section[2] for section in tfidfScores)

print("Document 1 Score:", doc1Score)
print("Document 2 Score:", doc2Score)
print("Document 3 Score:", doc3Score)

# Calculate and print the precision and recall of the model by considering that the search engine will return all
# documents with scores >= 0.1. --> add your Python code here

# the precision and recall:
newScores = []
docScores = [doc1Score, doc2Score, doc3Score]
for score in docScores:
    if score > .1:
        score = 1
    else:
        score = 0
    newScores.append(score)

print(f"Because we have document scores of {newScores}, that means our precision and recall are as follows:")
print(f" precision = ([doc1Score + doc3Score] / [doc1Score + doc3Score] + 0)")
print(f" recall = ([doc1Score + doc3Score] / [doc1Score + doc3Score] + 0)")
print(f"Both are 0 for b and c because there are no relevant and not retrieved values(c) and no irrelevant and "
      f"retrieved values(b) ")
print(f"Precision = [2 / (2+0)] * 100 = 100%")
print(f"Recall = [2 / (2+0)] * 100 = 100%")

