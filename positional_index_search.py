import os
from nltk.stem import PorterStemmer
ps = PorterStemmer()


def reading_corpus():
    stopfile = open("Stopword-List.txt", "r")
    stopwords = [word for line in stopfile for word in line.split()]
    dirr = os.getcwd()
    file = os.path.join(dirr, "TrumpSpeechs")
    punctuations = '''!()-[]{};:'",<>./?@#$%^&*_~'''
    docid = 0
    index_list = {}
    while docid < 56:
        file1 = os.path.join(file, "speech_"+str(docid)+".txt")
        f = open(file1, "r")
        filtered_words = preprocessing(f, stopwords, punctuations)
        index_list = create_index(index_list, filtered_words, docid)
        docid += 1
    return index_list


def preprocessing(f, stopwords, punctuations):
    no_punc = ' '
    for line in f:
        line = line.strip()
        line = line.lower()
        for char in line:
            if char not in punctuations:
                no_punc += char
        words = no_punc.split(" ")
    words = [ps.stem(word) for word in words]
    filtered_words = [word for word in words if word not in stopwords]
    filtered_words = [word for word in filtered_words if word != ""]
    return filtered_words


def create_index(index_list, filtered_words, id):
    for pos, term in enumerate(filtered_words):
        if term not in index_list:
            index_list[term] = []
            index_list[term].append(1)
            index_list[term].append({})
            index_list[term][1][id] = [pos]
        else:
            index_list[term][0] += 1
            if id not in index_list[term][1]:
                index_list[term][1][id] = [pos]
            else:
                index_list[term][1][id].append(pos)
    return index_list


dictionary = reading_corpus()


def pos_intersect(p1, p2, k):
    answer = []  # will store documents which satisfy the condition
    len1 = len(p1)  # length of posting list of of first word
    len2 = len(p2)  # length of posting list of of second word
    i = j = 0
    docs1 = []
    docs2 = []
    for doc in p1.keys():
        docs1.append(doc)  # elements(docs) of posting list of first word
    for doc in p2.keys():
        docs2.append(doc)   # elements(docs) of posting list of second word
    while i != len1 and j != len2:
        if docs1[i] == docs2[j]:    # if both word occurs in same document
            pp1 = p1[docs1[i]]  # list of positions where 1st word occurs in doc i
            pp2 = p2[docs2[j]]  # list of positions where 2nd word occurs in doc j
            plen1 = len(pp1)    # length of position list of 1st word in doc i
            plen2 = len(pp2)    # length of position list of 2nd word in doc j
            ii = jj = 0
            while ii != plen1 and jj != plen2:  # while (pp1 != nil and pp2 != nil)
                if pp2[jj] - pp1[ii] == k:  # if (pos(pp2) - pos(pp1) == k)
                    answer.append(docs1[i])  # add document in the answer
                    jj += 1  # pp2 <- next(pp2)
                    ii += 1  # pp1 <- next (pp1)
                elif pp2[jj] > pp1[ii]:  # else if (pos(pp2) > pos(pp1))
                    ii += 1
                else:
                    jj += 1
            i += 1  # next doc in position list of 1st word
            j += 1  # next doc in position list of 2st wor
        elif docs1[i] < docs2[j]:  # else if (docID(p1) < docID(p2))
            i += 1  # p1 <- next(p1)
        else:
            j += 1  # p2 <- next(p2)

    return answer


def making_query(query):
    print(query)
    query_list1 = query.split(" ")
    k = query_list1[1].split('/')
    query_list = [word for word in query_list1]
    print(query_list)
    k1 = int(k[1])
    query_list[0] = ps.stem(query_list[0])
    k[0] = ps.stem(k[0])
    answer = pos_intersect(dictionary[query_list[0]][1], dictionary[k[0]][1], k1 + 1)
    answer = list(dict.fromkeys(answer))  # removing the duplicate documents from list
    print(answer)
    return answer

def main():
   # dictionary = reading_corpus()
    with open('pos-dictionary', 'w') as f:
        for key, value in dictionary.items():
            f.write('%s:%s\n' % (key, value))
    answer = making_query()


if __name__ == '__main__':
    main()