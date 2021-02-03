from nltk.stem import PorterStemmer
ps = PorterStemmer()
dictionary = {}
with open('dictionary', "r") as file:
    rows = (line.split(':') for line in file)
    for row in rows:
        row[1] = row[1].strip()
        res = row[1].strip('][').split(', ')
        dictionary[row[0]] = res
for terms in dictionary:
    dictionary[terms] = list(map(int, dictionary[terms]))

                                    ###############
                # MADE THESE FUNCTIONS WHEN I STATED FOR SIMPLE QUERIES. MUCH MORE EFFICEINT
                # AS QUERIES WERE SOLVED ON THE ASCENDING ORDER OF LENTH OF THERI POSTING LIST
                # COULDN'T USE THEM FOR COMPLEX QUEIRES
                                    ##############
# def sort_by_num_postings(query_list, index_list):
#     new_dict = {}
#     for word in query_list:
#         new_dict[word] = len(index_list[word])
#     new_dict = sorted(new_dict, key=new_dict.get)
#     return new_dict
#
#
# def intersect(list1, list2):
#     intersect1 = []
#     i = 0
#     j = 0
#     while i < len(list1) and j < len(list2):
#         if list1[i] == list2[j]:
#             intersect1.append(list1[i])
#             i += 1
#             j += 1
#         elif list1[i] < list2[j]:
#             i += 1
#         else:
#             j += 1
#     return intersect1


def convert_to_postfix(query_list):
    ope = []   # operand list
    postfix = []
    for word in query_list:

        if word == '(':
            ope.append('(')
        elif word == ')':
            temp = ope.pop()
            while temp != '(':
                postfix.append(temp)
                temp = ope.pop()

        elif word == 'AND' or word == 'OR' or word == 'NOT':

            ope.append(word)
        else:
            postfix.append(word)

    for word in ope:
        postfix.append(word)
    return postfix


def query_eval(postfix):
    opertaions = ['AND', 'OR', 'NOT']
    operand_list = []
    operator_list = []
    ans = []  # storing result
    for word in postfix:
        if word not in opertaions:
            operand_list.append(word)
        else:
            operator_list.append(word)
    c = len(operand_list)  # counter
    c -= 1
    operand_list = [ps.stem(word) for word in operand_list]
    print('operation list', operator_list)
    print('operand list', operand_list)
    for i, word in enumerate(operand_list):
        operand_list[i] = dictionary[word]
    if len(operator_list) == 0:
        ans = operand_list[c]
    else:
        for word in operator_list:
            if word == 'OR':
                if len(ans) == 0:
                    ans = operand_list[c] + operand_list[c - 1]
                    c -= 2
                else:
                    ans += operand_list[c]
                    c -= 1
            if word == 'AND':
                if len(ans) == 0:
                    temp = [val for val in operand_list[c] if val in operand_list[c - 1]]
                    ans = temp
                    c -= 2
                else:
                    temp = [val for val in operand_list[c] if val in ans]
                    ans = temp
                    c -= 1
            if word == 'NOT':
                ans = [val for val in range(56) if val not in ans]
    ans = list(dict.fromkeys(ans))
    return ans


def make_query():
    query = 'outdated AND ( personnel OR policies )'
    query_list = query.split(" ")
    postfix = convert_to_postfix(query_list)
    ans = query_eval(postfix)
    print('document:', ans)
    print('no. of documents', len(ans))

    # token = sort_by_num_postings(query_list, dictionary)
    # if len(token) == 1:
    #     print(dictionary[token[0]])
    #     print('no of documents', len(dictionary[token[0]]))
    # elif len(token) == 2:
    #     result = intersect(dictionary[token[0]], dictionary[token[1]])
    #     print('result', result)
    #     print('no of documents', len(result))
    # else:
    #     print('nill')


def main():
           ###################
           #Reading from DISK(DICTIOANRY)#
           ####################
    # dictionary = {}
    # with open('dictionary', "r") as file:
    #     rows = (line.split(':') for line in file)
    #     for row in rows:
    #         row[1] = row[1].strip()
    #         res = row[1].strip('][').split(', ')
    #         dictionary[row[0]] = res
    # for terms in dictionary:
    #     dictionary[terms] = list(map(int, dictionary[terms]))


        ###################
        # making query#
        ####################
    make_query()


if __name__ == '__main__':
    main()