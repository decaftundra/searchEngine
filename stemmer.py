import nltk
import json
import file_handler
from nltk.stem.porter import *
from nltk.stem.lancaster import *

def main():
    str_txt = openFile()
    split_text = str_txt
    
    #lemma_vocab = vocab_lemmatize(split_text)
    #file_handler.write_json_file(lemma_vocab, 'library/lemma_vocab.txt')

    porter_vocab = vocab_stemmer_porter(split_text)
    file_handler.write_json_file(porter_vocab, "library/porter_vocab.txt" )



    return

def lancaster_stemming(split_text):
    
    lancaster_stemmed_vocab = {}
    lancaster_stemmer= LancasterStemmer()
    
    vocab = []

    for word in split_text:
        if word not in vocab:
            vocab.append(word)
            oldId = vocab.index(word)
            lancaster_stemmed_word = lancaster_stemmer.stem(word)
            if lancaster_stemmed_word in lancaster_stemmed_vocab:
                lancaster_stemmed_vocab[lancaster_stemmed_word].append(word)
            else:
                lancaster_stemmed_vocab.update({lancaster_stemmed_word:[word]})

    return lancaster_stemmed_vocab

def vocab_stemmer_porter(split_text):
    porter_stemmed_vocab = {}
    
    
    porter_stemmer = PorterStemmer()

    vocab = file_handler.open_json_file("library/vocab1.txt")

    for word in split_text:
        
        
        oldId = vocab.index(word)
        porter_stemmed_word = porter_stemmer.stem(word)
            

        if porter_stemmed_word in porter_stemmed_vocab:
            porter_stemmed_vocab[porter_stemmed_word].append(oldId)
        else:
            porter_stemmed_vocab.update({porter_stemmed_word:[oldId]})
    
    return porter_stemmed_vocab

def vocab_lemmatize(split_text):
    lemmatized_vocab = {}
    
    lemmatizer = nltk.WordNetLemmatizer()

    vocab = file_handler.open_json_file("library/vocab1.txt")

    for word in split_text:

        oldId = vocab.index(word)
        lemmatized_word = lemmatizer.lemmatize(word)

        if lemmatized_word in lemmatized_vocab:
            lemmatized_vocab[lemmatized_word].append(oldId)
        else:
            lemmatized_vocab.update({lemmatized_word:[oldId]})

    return lemmatized_vocab

def porter_word_stemmer(word_list):
    stemmed_list = []
    porter_word_stemmer = PorterStemmer()

    for word in word_list:

        porter_stemmed_word = porter_word_stemmer.stem(word)
        stemmed_list.append(porter_stemmed_word)


    return stemmed_list

def word_lemmatizer(word_list):
    lemma_list = []
    lemmatizer = nltk.WordNetLemmatizer()

    for word in word_list:

        lemmatized_word = lemmatizer.lemmatize(word)
        lemma_list.append(lemmatized_word)


    return lemma_list


    


            
def openFile():
    text = open('library/vocab1.txt', 'r')
    str_txt = json.load(text)
    return str_txt

if __name__ == '__main__':
    main()