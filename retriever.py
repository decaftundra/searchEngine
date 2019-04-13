#!/usr/bin/python3
# needs improving to remove forced type conversions

import sys
import math
import re
import json
from indexer import read_index_files as read_index_files_fromIndexer
import stemmer
import file_handler

# global declarations for doclist, postings, vocabulary
docids = []
postings = {}
vocab = []
doclength = {}
docTitles = {}
stemmed_vocab = {}
lemma_vocab = {}


def main():
	# code for testing offline
	if len(sys.argv) < 2:
		print('usage: ./retriever.py term [term ...]')
		sys.exit(1)
	query_terms = sys.argv[1:]
	answer = []

	read_index_files()

	#answer = retrieve_bool(query_terms)
	#answer = cosineScore(query_terms)

	# print('Query: ', query_terms)
	# i = 1
	# for docid in answer:

	# 	print(i, docids[int(docid)])
	# 	i += 1

def cos_retriever(list_query):
	answer = []
	scores = {}
	read_index_files()
	answer, scores = cosineScore(list_query)

	return answer, scores

def cos_retriever_title(list_query):
	answer = []
	scores = {}
	read_index_files()
	answer, scores = cosineScore_title_weighing_score_return(list_query)

	return answer, scores

def get_url(id):
	docids =file_handler.open_json_file("library/docids1.txt")
	return docids[int(id)]


def read_index_files():
	# reads existing data from index files: docids, vocab, postings
	# uses JSON to preserve list/dictionary data structures
	# declare refs to global variables
	global docids
	global postings
	global vocab
	global doclength
	

	# call read_index_files() from indexer.py
	docids, postings, vocab, doclength = read_index_files_fromIndexer()

	return

def cosineScore(query):
	global doclength
	global postings
	scores = {}
	
	no_of_docs = len(doclength)
	
	for term in query:
		term = term.lower()
		term = re.sub(r'[^\w*]', '', term)
		try:
			termid = vocab.index(term)
		except:
			print("\"",term, "\"is", 'is not in dictionary')
			continue
		no_docs_with_term = len(postings[str(termid)])
		idf = calculate_idf(no_of_docs, no_docs_with_term)
		posting_list = postings[str(termid)]
		for doc_id in posting_list:
			tf = calculate_tf(posting_list[doc_id], doclength[doc_id])
			idf_tf_weight = tf*idf
			update_score(scores, doc_id, idf_tf_weight)
	answer = list(sorted(scores, key=lambda x: scores[x], reverse = True))

	return answer, scores

def cosineScore_title_weighing(query):
	global doclength
	global postings
	docTitles = file_handler.open_json_file("library/doctitles1.txt")
	scores = {}
	
	no_of_docs = len(doclength)
	
	for term in query:
		term = term.lower()
		term = re.sub(r'[^\w*]', '', term)
		try:
			termid = vocab.index(term)
		except:
			print("\"",term, "\"is", 'is not in dictionary')
			continue
		no_docs_with_term = len(postings[str(termid)])
		idf = calculate_idf(no_of_docs, no_docs_with_term)
		posting_list = postings[str(termid)]
		for doc_id in posting_list:
			tf = calculate_tf(posting_list[doc_id], doclength[doc_id])
			idf_tf_weight = tf*idf
			update_score(scores, doc_id, idf_tf_weight)
			score_title(termid, doc_id, docTitles, scores)
	answer = list(sorted(scores, key=lambda x: scores[x], reverse = True))

	return answer

def cosineScore_title_weighing_score_return(query):
	global doclength
	global postings
	docTitles = file_handler.open_json_file("library/doctitles1.txt")
	scores = {}
	
	no_of_docs = len(doclength)
	
	for term in query:
		term = term.lower()
		term = re.sub(r'[^\w*]', '', term)
		try:
			termid = vocab.index(term)
		except:
			print("\"",term, "\"is", 'is not in dictionary')
			continue
		no_docs_with_term = len(postings[str(termid)])
		idf = calculate_idf(no_of_docs, no_docs_with_term)
		posting_list = postings[str(termid)]
		for doc_id in posting_list:
			tf = calculate_tf(posting_list[doc_id], doclength[doc_id])
			idf_tf_weight = tf*idf
			update_score(scores, doc_id, idf_tf_weight)
			score_title(termid, doc_id, docTitles, scores)
	answer = list(sorted(scores, key=lambda x: scores[x], reverse = True))

	return answer, scores

def score_title(termId, docId, docTitles, scores):
	
	termId_list = docTitles[docId]

	if termId in termId_list:
		scores[docId] = scores[docId]*2
	
	return 

def porter_stemming_retrieval(query):
	global stemmed_vocab
	postings = file_handler.open_json_file("library/postings1.txt")
	final_list = []
	stemmed_query = stemmer.porter_word_stemmer(query)
	
	stemmed_vocab = file_handler.open_json_file("library/porter_vocab.txt")

	for word in stemmed_query:
		word = re.sub(r'[^\w*]', '', word)
		word = word.lower()
		if word in stemmed_vocab:
			old_ID_list = stemmed_vocab[word]
			for id in old_ID_list:
				list_of_ID = list(postings[str(id)].keys())
				for id in list_of_ID:
					final_list.append(id)
	
	return final_list 

def porter_stemming_retrieval_cos(query):
	global stemmed_vocab
	vocab = file_handler.open_json_file("library/vocab1.txt")
	
	
	expended_query = []
	for word in query:
		i = query.index(word)
		word = re.sub(r'[^\w*]', '', word)
		word = word.lower()
		query[i] = word
	
	stemmed_query = stemmer.porter_word_stemmer(query)


	stemmed_vocab = file_handler.open_json_file("library/porter_vocab.txt")

	for word in stemmed_query:
		
		if word in stemmed_vocab:
			old_ID_list = stemmed_vocab[word]
			for id in old_ID_list:
				expended_query.append(vocab[id])
				
	answer, scores = cos_retriever_title(expended_query)
	return answer, scores

def lemmatize_retrieval(query):
	global lemma_vocab
	postings = file_handler.open_json_file("library/postings1.txt")
	final_list = []
	lemma_query = stemmer.word_lemmatizer(query)
	lemma_vocab = file_handler.open_json_file("library/lemma_vocab.txt")

	for word in lemma_query:
		word = word.lower()
		word = re.sub(r'[^\w*]', '', word)
		if word in lemma_vocab:
			old_ID_list = lemma_vocab[word]
			for id in old_ID_list:
				list_of_ID = list(postings[str(id)].keys())
				for id in list_of_ID:
					final_list.append(id)
	
	return final_list




def update_score(dict_scores, doc_id, score):
	
	if doc_id not in dict_scores:
		dict_scores.update({doc_id:score})
	else:
		dict_scores[doc_id]+= score
	return

def calculate_tf(frequency_in_doc, doc_length):	
	return frequency_in_doc/doc_length

def calculate_idf(no_of_docs, no_docs_with_term):
	return math.log10(no_of_docs/no_docs_with_term)


#  a function to perform Boolean retrieval with ANDed terms
def retrieve_bool(query_terms):

	

	#### your code starts here ####
	global postings
	global vocab
	global docids

	answer = []
	bool_operator = ''

	# try the first term of query
	try: 
		termid = str(vocab.index(query_terms[0]))
		posting_list = []
		
		posting_list = list(postings[termid])

		for oneDoc in posting_list:
		    	answer.append(oneDoc)
	except:
		print(query_terms[0], "is not in dictionary")
	
	finally:
		# avoid to redo the first term of query
		query_terms.pop(0) 


	# process the other terms of query
	for term in query_terms: 
		if term in ('AND', 'OR', 'NOT'):
			bool_operator = term
			continue

		#try the next term. Raises exception if the term not in vocab
		try: 
			termid = str(vocab.index(term))
			posting_list = list(postings[termid])

		except:
			print(term, ' is not in dictionnary')
			continue

		if bool_operator == 'OR':

			bool_operator, answer = or_function(posting_list, answer)

		elif bool_operator == 'NOT':

			bool_operator, answer = not_function(posting_list, answer)

		elif bool_operator == 'AND' or bool_operator == '': #assume anded terms if no operator

			bool_operator, answer = and_function(posting_list, answer)

	return answer

# function that applies the ORed terms on answer
def or_function(posting_list, answer):
    for posting in posting_list:
            answer.append(posting)
            answer = sorted(list(set(answer)))

    bool_operator = ''

    return bool_operator, answer

# function that remove postings of terms following operator NOT from answer
def not_function(posting_list, answer):
    for posting in posting_list:
            if posting in answer:
                    answer.remove(posting)

            bool_operator = ''

    return bool_operator, answer

# function that applies the ANDed terms on answer
def and_function(posting_list, answer):
    temp_list = list(answer)
    answer = []
    for posting in posting_list:
            if posting in temp_list:
                    answer.append(posting)

    answer = sorted(list(set(answer)))
    temp_list = []
    bool_operator = ''

    return bool_operator, answer

# Standard boilerplate to call the main() function
if __name__ == '__main__':
    main()