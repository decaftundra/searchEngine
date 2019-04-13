# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#!/usr/bin/python3	indexer.py -d ./LookingGlass 5

import sys
import os
import re
import json
import math
from nltk import word_tokenize
from nltk.corpus import stopwords

# global declarations for docids, lengths, postings, vocabulary
docids = []
doclength = {}
postings = {}
vocab = []
docTitles = {}

def main():
	# code only for testing offline only - not used for a crawl
    max_files = 64000;
    if len(sys.argv) == 1:
        print ('usage: ./indexer.py file | -d directory [maxfiles]')
        sys.exit(1)
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
    elif len(sys.argv) == 3:
        if re.match('-d', sys.argv[1]):
            dirname = sys.argv[2]
            dir_index = True
        else:
            print ('usage: ./indexer.py file | -d directory [maxfiles]')
            sys.exit(1)
    elif len(sys.argv) == 4:
        if re.match('\d+', sys.argv[3]):
            max_files = int(sys.argv[3])
        else:
            print ('usage: ./indexer.py file | -d directory [maxfiles]')
            sys.exit(1)
    else:
        print ('usage: ./indexer.py file | -d directory [maxfiles]')

    if len(sys.argv) == 2:
        index_file(filename)
    elif re.match('-d', sys.argv[1]):
        for filename in os.listdir(sys.argv[2]):
            if re.match('^_', filename):
                continue
            if max_files > 0:
                max_files -= 1
                filename = sys.argv[2]+'/'+filename
                index_file(filename)
            else:
                break
				
    write_index_files(1)
			
def index_file(filename):	# code only for testing offline only - not used for a crawl
    try:
        input_file = open(filename, 'rb')
    except (IOError) as ex:
        print('Cannot open ', filename, '\n Error: ', ex)
    else:
        page_contents = input_file.read() # read the input file
        url = 'http://www.'+filename+'/'
        #print (url, page_contents)
        make_index(url, page_contents)   
        input_file.close()

	
def write_index_files(n):

	# n can be 0,1
	# declare refs to global variables
    global docids
    global postings
    global vocab
    global doclength
    global docTitles
	# decide which files to open
	# there are 2 sets, written to on alternate calls
    nn = n+1
	
    try:
        open("library", 'r')
    except:
        os.makedirs("library", exist_ok=True)

    # open files
    out_d = open('library/docids'+str(nn)+'.txt', 'w')
    out_l = open('library/doclength'+str(nn)+'.txt', 'w')
    out_v = open('library/vocab'+str(nn)+'.txt', 'w')
    out_p = open('library/postings'+str(nn)+'.txt', 'w')
    out_dt = open('library/doctitles'+ str(nn)+ '.txt', 'w')
	# write to index files: docids, vocab, postings
	# use JSON as it preserves the dictionary structure (read/write treat it as a string)
    json.dump(docids, out_d)
    json.dump(doclength, out_l)
    json.dump(vocab, out_v)
    json.dump(postings, out_p)
    json.dump(docTitles, out_dt)
	# close files
    out_d.close()
    out_l.close()
    out_v.close()
    out_p.close()
    out_dt.close()
	
    d = len(docids)
    v = len(vocab)
    p = len(postings)
    dt = len(docTitles)
    print ('===============================================')
    print ('Indexing: ', d, ' docs ', v, ' terms ', p, ' postings lists written to file', dt, 'doc Titles written to file')
    print ('===============================================')
	
    return
	
def read_index_files():

	# declare refs to global variables
    global docids
    global postings
    global vocab
    global doclength
    
    nn = 1	

	# reads existing data into index files: docids, lengths, vocab, postings
    in_d = open('library/docids'+str(nn)+'.txt', 'r') 
    in_l = open('library/doclength'+str(nn)+'.txt', 'r')
    in_v = open('library/vocab'+str(nn)+'.txt', 'r')
    in_p = open('library/postings'+str(nn)+'.txt', 'r')
    
	
    docids = json.load(in_d)
    doclength = json.load(in_l)
    vocab = json.load(in_v)
    postings = json.load(in_p)
    

    in_d.close()
    in_l.close()
    in_v.close()
    in_p.close()
    
    return docids, postings, vocab, doclength



def clean_html(html):
	##########################################
	#####   remove markup from page      #####
	#### your code here ####
    # code from Dan Smith

    #find the titles and headings
    title = re.findall(r"<title>(.*?)</title>", html)
    title = re.findall(r"<h\d>(.*?)</h\d>", html)

    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    

    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    cleaned = re.sub(r"[!()-[]{};:'""\,<>./?@#$%^&*_~]+", " ", cleaned)
    cleaned = re.sub(r"&\w+;", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)  
    
    cleaned = cleaned.strip()
	#####  end of remove markup from page #####
   ##########################################
    return cleaned, processTitle(title)
	

	
def make_index(url, page_contents):
	# declare refs to global variables
    global docids		# contains URLs + docids
    global postings		# contains wordids + docids, frequencies
    global vocab		# contains words + wordids
    global doclength	# contains docids + lengths
  
    print ('make_index: url = ', url)
	#print ('make_index1: page_text = ', page_text) # for testing

	#### extract the words from the page contents ###
    if (isinstance(page_contents, bytes)): # convert bytes to string if necessary
        page_contents = page_contents.decode('utf-8','ignore') # ignore code errors...

	#### page_text is the initial content, transformed to words ####
    page_str, page_title = clean_html(page_contents)
    re.sub(r'[^\w*]', ' ', page_str)
    stopWords = set(stopwords.words('english'))
    page_text = word_tokenize(page_str)
    for word in page_text:
        if len(word) < 2 or word in stopWords:
            page_text.remove(word)
    #page_text = page_str.split()
 
    #############################################
	#####   add the url to the doclist      #####
	#### your code here ####
    url = re.sub('(https|http)(\W*)(www.)', '', url)
    if url not in docids:
        docids.append(url)
    currentDocId = len(docids)-1
    doclength.update({currentDocId:len(page_text)})
    #####  end of add the url to the doclist #####
	##############################################

	#####  add entries to the index    ####
	#
	# split the words string into a list
	# store doclength
	# add the vocab counts and postings
	#### your code here ####
    
    for str in page_text:
        str = re.sub(r'[^\w]', '', str) # remove special character at beginning and end of words
        str = str.lower()
        if str not in vocab:
            if len(str) > 1: #discard one letter word
                
                vocab.append(str) #add to vocab
                currentWordId = len(vocab)-1               
                create_posting_entry(currentWordId, currentDocId) #create a posting with the new wordID 
        elif str in vocab:    
            update_posting_entry(vocab.index(str),currentDocId) #update existing posting

    create_docTitle_entry(currentDocId)

    for word in page_text:
        if len(word) < 2 or word in stopWords:
            page_text.remove(word)

    for str in page_title:
        
        
        if str in stopWords:
            page_title.remove(str)
            continue
        str = re.sub(r'[^\w]', '', str)
        str = str.lower()

        termID = 0
        if str not in vocab:
            if len(str)> 1:
                vocab.append(str)
                termID = len(vocab)-1               
                create_posting_entry(termID, currentDocId)
        else:
            termID = vocab.index(str)
        
        update_docTitle_postings(termID, currentDocId)
        

            

	#####  end of add entries to the index   #####
	##############################################


	##### save the index after every 100 documents ####
    if (len(doclength)%100 == 0): # 
        n = int(len(doclength)/100)%2
        write_index_files(n)
    write_index_files(0)
    return

#create a posting in dictionnary with the termID and docID {termID:{docID:frequency}}
def create_posting_entry (termId, docId):
    global postings

    postings.update({termId:{docId:1}})
    return

#update a posting in dictionnary with the termID and docID {termID:{docID:frequency}}
def update_posting_entry (termId, docId):
    global postings
    if docId not in postings[termId]: #if this docID doesn't exist for that term, create the entry for docID
        postings[termId].update({docId:1})
    else:
        postings[termId][docId]+=1 #if word already exists for that docID, update frequency

    return

def processTitle(title):

    list_word = []
    for str in title:
        

        for word in str.split():
            if len(word)> 1:
                list_word.append(word)
    
    return list_word 

def update_docTitle_postings(termID, docID):
    global docTitles
    
    if termID not in docTitles[docID]:
        docTitles[docID].append(termID)
    return

def create_docTitle_entry(docID):
    global docTitles

    docTitles.update({docID:[]})
    return

	
# Standard boilerplate to call the main() function
if __name__ == '__main__':
    main()


	
