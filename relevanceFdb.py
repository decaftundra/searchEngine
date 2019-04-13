import retriever
import pooling

def main():
    listA, scoreA = retriever.cos_retriever_title(["pension", "query", "contact"])
    listB, scoreB = retriever.porter_stemming_retrieval_cos(["pension", "query", "contact"])
    finalList, finalScore = compare_list(listA, listB, scoreA, scoreB)
    pooling.print_answer(finalList)
    
    return

def relevance_feedback(query):
    listA, scoreA = retriever.cos_retriever(query)
    listB, scoreB = retriever.cos_retriever_title(query)
    finalList, finalScore = compare_list(listA, listB, scoreA, scoreB)
    listA, scoreA = retriever.porter_stemming_retrieval_cos(query)
    finalList, finalScore = compare_list(listA, finalList, scoreA, finalScore)
    
    pooling.print_answer(finalList)


def compare_list(listA, listB, scoreA, scoreB):
    
    finalScore = {}

    if len(listB)< len(listA):
        listA, listB, scoreA, scoreB = swapLists(listA, listB, scoreA, scoreB)

    for i in range(0 , len(listA)):
        if listA[i] in scoreB:
            finalScore.update({listA[i]:scoreA.pop(listA[i])+scoreB.pop(listA[i])})
        else:
            finalScore.update({listA[i]:scoreA[listA[i]]})
    
    finalScore.update(scoreB)
    finalList = list(sorted(finalScore, key=lambda x: finalScore[x], reverse = True))    


    return finalList, finalScore

def swapLists(listA, listB, scoreA, scoreB):
    tempList = listA
    listA = listB
    listB = tempList
    tempScore = scoreA
    scoreA = scoreB
    scoreB = tempScore

    return listA, listB, scoreA, scoreB

if __name__ == "__main__":
    main()