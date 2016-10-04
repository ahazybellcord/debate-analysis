# -*- coding: utf-8 -*-

import re
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from collections import Counter
from nltk.book import Text

special_words = ['I', 'Lester', 'Holt', 'Hillary', 'Clinton', 'Donald', 'Trump', 'Mr', 'Secretary', 'OK', 'ISIS',
                 'China', 'Sidney', 'Blumenthal', 'Republicans', 'NAFTA', 'Iran', 'Sean']

capitalized_words = ["I", "I'd", "I'll", "I'm", "I've", "Mr.", "Donald", "Trump", "Lester", "Secretary", "Hillary",
                     "OK", "China", "Iran", "NAFTA", "Republicans"]

special_tokens = ["Mr.", "J.", "St."]

nonword_tokens = [",", ":", ";", "-", "—", "...", "\"", "'"]


def main():
    words = get_words_from_file('debate_transcript2.txt')

    holt_words, clinton_words, trump_words = partition_words(words, "HOLT", "CLINTON", "TRUMP")

    holt_words = separate_nonword_tokens(holt_words)
    clinton_words = separate_nonword_tokens(clinton_words)
    trump_words = separate_nonword_tokens(trump_words)

    holt_text = Text(holt_words)
    clinton_text = Text(clinton_words)
    trump_text = Text(trump_words)

    #######
    exit(0)
    #######

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

    common_tuples.sort(key=(lambda x: x[0]), reverse=True)

    filtered_tuples = [item for item in common_tuples if item[0] > 50]

    interesting_words = ['they', 'very', 'because', 'what', 'think', 'would', 'be', 'great', 'bad', 'worst', 'look']

    for word in interesting_words:
        print(word.upper())
        print('Trump frequency: ' + str(trump_dictionary[word]))
        print('Trump percentage: ' + str(round(100 * trump_dictionary[word] / len(trump_words), 2)) + '%')
        print('Clinton frequency: ' + str(clinton_dictionary[word]))
        print('Clinton percentage: ' + str(round(100 * clinton_dictionary[word] / len(clinton_words), 2)) + '%')

    create_frequent_histogram(trump_dictionary, 50, 'Most frequent words used by Trump in first debate', 'r')

    create_frequent_histogram(clinton_dictionary, 37, 'Most frequent words used by Clinton in first debate', 'b')

    create_interlocking_frequent_histogram(filtered_tuples, 'Most freq words', 'r')

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

    # print(' '.join(foldin))
    # print('~~~~~~~~~~~~~~~~~~~')
    # just Trump words
    cutup = []
    for word in trump_words:
        cutup.append(word)
    random.shuffle(cutup)
    # print(' '.join(cutup))


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
    moderator_words, candidateA_words, candidateB_words = [], [], []

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


# split up words with non-letter characters
# for use with nltk Text
def separate_nonword_tokens(words):
    separated_words = []
    for word in words:
        quoted_match = re.search(r'(?P<open_quote_only>")(?P<after_word>\w+)|(?P<before_word>\w+)'
                                 r'(?P<close_quote_only>")|(?P<open_quote>")(?P<between_word>\w+)'
                                 r'(?P<close_quote>")', word)
        punctuated_match = re.search(r'(?P<open_quote>"?)(?P<word>\w+)(?P<punctuation>[.,;:?!]|\.\.\.)'
                                     r'(?P<close_quote>"?)', word)
        apostrophe_match = re.search(r'(?P<open_quote>"?)(?P<first_part>\w*)(?P<apostrophe>’)(?P<second_part>\w+)'
                                     r'(?P<punctuation>[.,;:?!]?|\.\.\.?)(?P<close_quote>"?)', word)
        if quoted_match:
            for token in quoted_match.groups():
                if token:
                    separated_words.append(token)
        if apostrophe_match:
            print(apostrophe_match.groups())
            for token in apostrophe_match.groups():
                if token:
                    separated_words.append(token)
        elif punctuated_match and not special_token(word):
            print(punctuated_match.groups())
            for token in punctuated_match.groups():
                if token:
                    separated_words.append(token)
        else:
            separated_words.append(word)
    return separated_words


def special_token(word):
    global special_tokens

    for token in special_tokens:
        if token in word:
            return True
    return False


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

    # matplotlib.rcParams['patch.facecolor'] = color

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
