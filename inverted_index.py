import os
from nltk.stem import PorterStemmer
ps = PorterStemmer()


def preprocessing(f, stopwords, punctuations):
    no_punc = ' '
    extra_line = f.readline()
    for line in f:
       # line = line.strip()
        line = line.lower()
        for char in line:
            if char not in punctuations:
                no_punc += char
        words = no_punc.split(" ")
    words = [ps.stem(word) for word in words]
    filtered_words = [word for word in words if word not in stopwords]
    filtered_words = [word for word in filtered_words if word != ""]  # removing empty words

    return filtered_words


def create_index(index_list, filtered_words, id):
    for term in filtered_words:
        if term not in index_list:
            index_list[term] = [id]
        else:
            if id not in index_list[term]:
                index_list[term].append(id)
    return index_list


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
    print('no. dictionary words ', len(index_list))
    return index_list


def main():
    dictionary = reading_corpus()
    with open('dictionary', 'w') as f:
        for key, value in dictionary.items():
            f.write('%s:%s\n' % (key, value))
    print(dictionary)


if __name__ == '__main__':
    main()

