'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 18, 2022.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as 
    described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    dot = 0
    for i in vec1.keys():
        # dot += list(vec1.values())[i]*list(vec2.values())[i]
        for j in vec2.keys():
            if i==j:
                dot += vec1[i]*vec2[j]
    vec1_square_sum = 0
    for i in range(len(vec1)):
        vec1_square_sum += list(vec1.values())[i]*list(vec1.values())[i]
    vec2_square_sum = 0
    for i in range(len(vec2)):
        vec2_square_sum += list(vec2.values())[i] * list(vec2.values())[i]

    return dot/math.sqrt(vec1_square_sum*vec2_square_sum)



def build_semantic_descriptors(sentences):
    # sentences = list of lists of strings
    # returns d = dictionary
    # d[w] = dictionary in a dictionary with how many times each other word
    # appears in the same sentence as w
    # update semantic descriptor sentence by sentence
    d = {}
    for sentence in sentences:
        word_in_sentence_list = []
        for word in sentence:
            if word not in word_in_sentence_list:
                if word not in d.keys():
                    d[word] = {}
                    sentence_words = []
                    for other_word in sentence:
                        if other_word != word and other_word not in sentence_words:
                            if other_word in d[word].keys():
                            # if it exists
                                d[word][other_word] += 1
                            else:
                                d[word][other_word] = 1
                            sentence_words.append(other_word)

                else: # if word is in d.keys
                    sentence_words = []
                    for other_word in sentence:
                        if other_word != word and other_word not in sentence_words:
                            if other_word in d[word].keys():
                                # if it exists
                                d[word][other_word] += 1
                            else:
                                d[word][other_word] = 1
                            sentence_words.append(other_word)
                word_in_sentence_list.append(word)
    return d

def build_semantic_descriptors_from_files(filenames):
    filecombined = []
    for i in range(len(filenames)):
        file_read = open(filenames[i], "r", encoding="UTF-8")

        # replaces w/ space
        file_read = file_read.read().replace(",", " ")
        file_read = file_read.replace("-", " ")
        file_read = file_read.replace("--", " ")
        file_read = file_read.replace(":", " ")
        file_read = file_read.replace(";", " ")
        file_read = file_read.replace("“", " ")
        file_read = file_read.replace("”", " ")
        file_read = file_read.replace("(", " ")
        file_read = file_read.replace(")", " ")
        file_read = file_read.replace("*", " ")
        file_read = file_read.replace("‘", " ")
        file_read = file_read.replace("‘‘", " ")
        file_read = file_read.replace("_", " ")

        # sentence seperating
        file_read = file_read.replace("!", ".") # split at all . , but cant split more thna once so make all punctuation as . and treat them the same
        file_read = file_read.replace("?", ".")
        file_read = file_read.strip().lower().split(".")
        # now we have sentences (but in an array)
        temp_thing = []
        for sent in file_read:
            temp_thing.append([sent])
        # split every word in every sentence
        for sent in temp_thing:
            for word_group in sent:
                k = word_group.split()
                filecombined.append(k)

    dict = build_semantic_descriptors(filecombined)
    return dict

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    # semantic_descriptors is the dict returned from function c)
    # word and choices are both in as semantic_descriptors[choices[i]]
    # or semantic_descriptors[word]
    # run cosine_similarity on semantic_descriptors[word]
    # and semantic_descriptors[i] for i in choices
    # if one of the words isnt in there, then return -1
    highest_similarity = -2 # anything <= -1
    best_choice = choices[0] # returns the first
    for i in choices:
        # either catch a KeyError or return -1
        try: similarity_fn(semantic_descriptors[i], semantic_descriptors[word])
        except KeyError:
            pass
        else:
            tmp = similarity_fn(semantic_descriptors[i], semantic_descriptors[word])
            if tmp > highest_similarity: # this way smallest index is chosen
                highest_similarity = tmp
                best_choice = i
    return best_choice

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    # convert each LINE (\n) of filename into an array
    filecombined = []
    file_read = open(filename, "r", encoding="UTF-8")

    # replaces w/ space
    file_read = file_read.read().replace(",", " ")
    file_read = file_read.replace("-", " ")
    file_read = file_read.replace("--", " ")
    file_read = file_read.replace(":", " ")
    file_read = file_read.replace(";", " ")
    file_read = file_read.replace("“", " ")
    file_read = file_read.replace("”", " ")
    file_read = file_read.replace("(", " ")
    file_read = file_read.replace(")", " ")
    file_read = file_read.replace("*", " ")
    file_read = file_read.replace("‘", " ")
    file_read = file_read.replace("‘‘", " ")
    file_read = file_read.replace("_", " ")

    # sentence seperating

    file_read = file_read.strip().lower().split("\n")
    # now we have sentences (but in an array)
    temp_thing = []
    for sent in file_read:
        temp_thing.append([sent])
    # split every word in every sentence
    for sent in temp_thing:
        for word_group in sent:
            k = word_group.split()
            filecombined.append(k)

    # now every sentence is an array and an element of filecombined
    # with every word as an element of the sentence array
    # extract the second element of each line's array
    answers = []
    for line in filecombined:
        answers.append(line[1])
        line.remove(line[1])
    # for every sentence run most similar word, then compare
    generated_answers = []
    for line in filecombined:
        ans = most_similar_word(line[0], line[1:], semantic_descriptors, similarity_fn)
        # append to a list GENERATED ANSWERS
        generated_answers.append(ans)

    correct_count = 0
    for idx in range(len(generated_answers)): # should be same len as answers
        if generated_answers[idx] == answers[idx]:
            correct_count+=1

    return 100*correct_count/len(generated_answers) # percentage

print(cosine_similarity({"b": 4, "c": 5, "d": 6},{"a": 1, "b": 2, "c": 3}))
sentences = [["i", "am", "a", "sick", "man"],
["i", "i", "am", "a", "spiteful", "man"],
["i", "am", "an", "unattractive", "man", "man", "man", "man"],
["i", "believe", "my", "liver", "is", "diseased"],
["however", "i", "know", "nothing", "at", "all", "about", "my",
"disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]
print(build_semantic_descriptors(sentences)["man"])
print(build_semantic_descriptors([['a','b','a','c','a'],['a','b']]))
# print(build_semantic_descriptors_from_files(["test.txt"]))

# sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
# res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
# print(res, "of the guesses were correct")
#
sem_descriptors = build_semantic_descriptors_from_files(["sentence1.txt", "sentence2.txt"])
res = run_similarity_test("answers.txt", sem_descriptors, cosine_similarity)
print(res, "of the guesses were correct")


def test_most_similar_word():
    sem_desc = {"dog": {"cat": 1, "food": 1}, "cat": {"dog": 1}}
    print(most_similar_word("dog", ["cat", "rat"], sem_desc, cosine_similarity))

test_most_similar_word()
