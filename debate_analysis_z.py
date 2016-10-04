# -*- coding: utf-8 -*-

import re
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from collections import Counter
from nltk.book import Text
#from nltk.book import Text

special_words = ['I', 'Lester', 'Holt', 'Hillary', 'Clinton', 'Donald', 'Trump', 'Mr', 'Secretary', 'OK', 'ISIS',
                     'China', 'Sidney', 'Blumenthal', 'Republicans', 'NAFTA', 'Iran', 'Sean']

capitalized_words = ["I", "I'd", "I'll", "I'm", "I've", "Mr.", "Donald", "Trump", "Lester", "Secretary", "Hillary",
                     "OK", "China", "Iran", "NAFTA", "Republicans"]

def main():

    words = get_words_from_file('debate_transcript2.txt')

    holt_words, clinton_words, trump_words = partition_words(words, "HOLT","CLINTON","TRUMP")

    separate_nonword_tokens(holt_words)
    #remove_nonwords(clinton_words)
    #remove_nonwords(trump_words)

    #decapitalize(holt_words)
    #decapitalize(clinton_words)
    #decapitalize(trump_words)

    trump_text = Text(trump_words)


    exit(0)

    lowercase_letters = [chr(c) for c in range(ord('a'), ord('z') + 1)]
    uppercase_letters = [chr(c) for c in range(ord('A'), ord('Z') + 1)]

    trump_dictionary = {}
    clinton_dictionary = {}

    for word in trump_words:
        if word in trump_dictionary:
            trump_dictionary[word] += 1
        else:
            trump_dictionary[word] = 1

    for word in clinton_words:
        if word in clinton_dictionary:
            clinton_dictionary[word] += 1
        else:
            clinton_dictionary[word] = 1

    common_tuples = []
    for item in trump_dictionary.keys():
        common_tuples.append((trump_dictionary[item], item, 'Trump'))
    for item in clinton_dictionary.keys():
        common_tuples.append((clinton_dictionary[item], item, 'Clinton'))

    common_tuples.sort(key=(lambda x:x[0]), reverse=True)

    filtered_tuples = [item for item in common_tuples if item[0] > 50]

    interesting_words = ['they','very','because','what','think','would', 'be', 'great', 'bad', 'worst','look']

    for word in interesting_words:
        print(word.upper())
        print('Trump frequency: ' + str(trump_dictionary[word]))
        print('Trump percentage: ' + str(round(100 * trump_dictionary[word] / len(trump_words), 2)) + '%')
        print('Clinton frequency: ' + str(clinton_dictionary[word]))
        print('Clinton percentage: ' + str(round(100 * clinton_dictionary[word] / len(clinton_words), 2)) + '%')

    create_frequent_histogram(trump_dictionary, 50, 'Most frequent words used by Trump in first debate','r')

    create_frequent_histogram(clinton_dictionary, 37, 'Most frequent words used by Clinton in first debate','b')

    create_interlocking_frequent_histogram(filtered_tuples, 'Most freq words', 'r')

    #######
    exit(0)
    #######

    sorted_trump_words = []
    for pair in sorted(trump_dictionary.items(), key=lambda x: x[1]):
        sorted_trump_words.append(pair)
    sorted_trump_words.reverse()

    print('TRUMP\'S WORDS')
    for word in sorted_trump_words:
        print("(" + str(word[0]) + ", " + str(word[1]) + ")")

    sorted_clinton_words = []
    for pair in sorted(clinton_dictionary.items(), key=lambda x: x[1]):
        sorted_clinton_words.append(pair)
    sorted_clinton_words.reverse()

    print('CLINTON\'S WORDS')
    for word in sorted_clinton_words:
        print("(" + str(word[0]) + ", " + str(word[1]) + ")")

    # cut-up/fold-in Trump/Clinton words

    foldin = []
    for word in trump_words:
        foldin.append(word)
    for word in clinton_words:
        foldin.append(word)
    random.shuffle(foldin)

    #print(' '.join(foldin))
    #print('~~~~~~~~~~~~~~~~~~~')
    # just Trump words
    cutup = []
    for word in trump_words:
        cutup.append(word)
    random.shuffle(cutup)
    #print(' '.join(cutup))

def parse_transcript():



    holt_lines, clinton_lines, trump_lines = [], [], []

    holt = False
    clinton = False
    trump = False

    # parse debate transcript
    with open('debate_transcript2.txt', 'r') as f:
        for line in f:
            if "HOLT:" in line:
                holt_lines.append(line.split('HOLT: ')[1].replace('\n', ''))
                holt, clinton, trump = True, False, False
            elif "CLINTON:" in line:
                clinton_lines.append(line.split('CLINTON: ')[1].replace('\n', ''))
                holt, clinton, trump = False, True, False
            elif "TRUMP:" in line:
                trump_lines.append(line.split('TRUMP: ')[1].replace('\n', ''))
                holt, clinton, trump = False, False, True
            else:
                if line != '\n':
                    if holt:
                        holt_lines.append(line.replace('\n', ''))
                    elif clinton:
                        clinton_lines.append(line.replace('\n', ''))
                    elif trump:
                        trump_lines.append(line.replace('\n', ''))
                    else:
                        print('Something unexpected')
                        print('Got line: ' + line)
    return holt_lines, clinton_lines, trump_lines

def get_words_from_file(filename):
    # read file replacing newlines with space
    with open(filename) as f:
        words = f.read().replace('\n', ' ')

    # split text into list of words
    words = words.split(' ')

    # remove empty words
    for word in words:
        if not word:
            words.remove(word)

    return words

# split text into each speaker's words
# the last three arguments are tokens delineating each
# speaker in the original text (e.g. "HOLT", "CLINTON", "TRUMP")
def partition_words(text, moderator, candidateA, candidateB):
    moderator_words = []
    candidateA_words = []
    candidateB_words = []

    # assume text begins with moderator
    current = moderator_words

    # switch when encountering new speaker token
    # otherwise append to current speaker's words
    for i in range(len(text)):
        if moderator in text[i]:
            current = moderator_words
        elif candidateA in text[i]:
            current = candidateA_words
        elif candidateB in text[i]:
            current = candidateB_words
        else:
            current.append(text[i])

    return moderator_words, candidateA_words, candidateB_words

def separate_nonword_tokens(words):
    for word in words:
        matchObj = re.search(r'\W*',word)
        if matchObj:
            print(word)




def decapitalize(words):
    global capitalized_words

    for i in range(len(words)):
        # look for ends of sentences
        matchObj = re.search(r'.*[.?!]',words[i])
        c = ''
        if '.' in words[i]:
            c = '.'
        elif '?' in words[i]:
            c = '?'
        elif '!' in words[i]:
            c = '!'
        if matchObj and i + 1 < len(words):
            print(c + ' ' + words[i+1])
            if words[i+1] not in capitalized_words:
                words[i+1] = words[i+1].lower()

def create_frequent_histogram(dictionary, min_occurrences, title, color):

    frequent_dictionary = {}
    for word in dictionary:
      if dictionary[word] > min_occurrences:
        frequent_dictionary[word] = dictionary[word]

    sorted_values = sorted(frequent_dictionary.values())
    sorted_keys = sorted(frequent_dictionary, key=frequent_dictionary.get)

    sorted_keys.reverse()
    sorted_values.reverse()

    indexes = np.arange(len(sorted_keys))

    matplotlib.rcParams['patch.facecolor'] = color

    plt.bar(indexes, sorted_values)
    plt.xticks(indexes + 0.3, sorted_keys)
    plt.xlabel('Word')
    plt.ylabel('Frequency')
    plt.title(title)

    plt.show()

def create_interlocking_frequent_histogram(filtered_tuples, title, othercolor):
    indexes = np.arange(len(filtered_tuples))


    #matplotlib.rcParams['patch.facecolor'] = color

    bar_list = plt.bar(indexes, [item[0] for item in filtered_tuples])
    for i in range(len(filtered_tuples)):
        if filtered_tuples[i][2] == 'Trump':
            bar_list[i].set_color(othercolor)
    plt.xticks(np.arange(len(filtered_tuples)) + 0.3, [item[1] for item in filtered_tuples])
    plt.xlabel('Word')
    plt.ylabel('Frequency')
    plt.title(title)

    plt.show()



main()
