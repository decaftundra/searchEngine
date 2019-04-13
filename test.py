import file_handler
import re
import indexer
import retriever
import pooling



def main():

   
    porter = file_handler.open_json_file("library/porter_vocab.txt")
    lemma = file_handler.open_json_file("library/lemma_vocab.txt")
    vocab = file_handler.open_json_file("library/vocab1.txt")

    print(len(porter))
    print(len(lemma))
    print(len(vocab))






    
    
    










if __name__ == "__main__":
    main()
