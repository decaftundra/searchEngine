import retriever
from nltk.corpus import wordnet
import relevanceFdb

def main():
    queries = read_queries()

    #cos_retrieval(queries)
    porter_stemming_retrieval(queries)
    #lemmatizing_retrieval(queries)
    #cos_retrieval_title(queries)
    #relevance_fbck(queries)

    return

def read_queries():
    splitted_queries= []
    queries = open('IR_queries.txt', 'r')
    list_of_queries = [line.rstrip('\n') for line in queries]
    for str in list_of_queries:
        

        splitted_queries.append(str.split()) 
    


    return splitted_queries

def cos_retrieval(queries):
    answer = []
    i = 1
    print("COS RETRIEVAL")
    for query in queries:
        print("Query ", i)
        answer, scores = retriever.cos_retriever(query)
        #print_answer(answer)
        print(len(answer))
        #print_answer_scores(answer, scores)
        i+= 1

    return answer, scores


def cos_retrieval_title(queries):
    answer = []
    scores = {}
    i = 1
    print("COS RETRIEVAL TITLE")
    for query in queries:
        print("Query ", i)
        answer, scores = retriever.cos_retriever_title(query)
        print_answer(answer)
        #print(len(answer))
        i+= 1

    return answer, scores

def porter_stemming_retrieval(queries):
    answer=[]
    i = 1
    print("PORTER STEMMING")
    for query in queries:
        print("Query ", i)
        answer, scores = retriever.porter_stemming_retrieval_cos(query)
        print_answer(answer)
        #print(len(answer))
        #print_answer_scores(answer, scores)
        i+= 1
    
    return answer

def lemmatizing_retrieval(queries):
    answer=[]
    i = 1
    for query in queries:
        print("Query boum ", i)
        answer = retriever.lemmatize_retrieval(query)
        print_answer(answer)
        i+= 1
    
    return answer

def relevance_fbck(queries):
    i = 1
    print("RELEVANCE FEEDBACK")
    for query in queries:
        print("Query ", i)
        relevanceFdb.relevance_feedback(query)
        
        i+= 1

def print_answer(answer):

    if len(answer) < 10:
        for i in range(0, len(answer)):
            print(retriever.get_url(answer[i]))
    else:
        for i in range(10):
            print(retriever.get_url(answer[i]))

def print_answer_scores(answer, scores):
    
    if len(answer) < 10:
        for i in range(0, len(answer)):
            print(retriever.get_url(answer[i]), "score: ", scores[answer[i]])
    else:
        for i in range(10):
            print(retriever.get_url(answer[i]), "score: ", scores[answer[i]])



if __name__ == "__main__":
    main()