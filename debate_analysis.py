# -*- coding: utf-8 -*-

import re
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from collections import Counter

special_words = ['I', 'Lester', 'Holt', 'Hillary', 'Clinton', 'Donald', 'Trump', 'Mr', 'Secretary', 'OK', 'ISIS',
                     'China', 'Sidney', 'Blumenthal', 'Republicans', 'NAFTA', 'Iran', 'Sean']

def main():

    holt_lines, clinton_lines, trump_lines = parse_transcript()

    '''
    for line in holt_lines:
        # print(line)
        # match a location or proper name
        matchObj = re.search(r'([A-Z][a-z]+, )?([A-Z][a-z]+ )+[A-Z][a-z]+', line)
        if matchObj:
            print("Found a location or name: ", matchObj.group())
        matchObj = re.search(r'[A-Z][a-z]+ ([A-Z]\. )?[A-Z][a-z]+', line)
        if matchObj:
            print("Found a name: ", matchObj.group())
    '''

    for line in trump_lines:
        matchObj = re.search(r'worst.*ever', line)
        if matchObj:
            print(line + '\n')

    #exit(0)

    holt_words = get_words_from_lines(holt_lines)
    clinton_words = get_words_from_lines(clinton_lines)
    trump_words =  get_words_from_lines(trump_lines)

    trump_superlative_count = 0
    trump_me_count = 0
    trump_black_and_white_count = 0

    superlatives = ['very', 'many', 'really', 'great', 'huge', 'extremely', 'tremendous', 'unbelievable', 'big', 'too']
    black_and_white = ['good', 'bad']

    # find consecutive words
    for i in range(len(trump_words) - 1):
        current = trump_words[i]
        if current in superlatives:
            trump_superlative_count += 1
        if current in black_and_white:
            trump_black_and_white_count += 1
        if 'I' in current or current == 'me':
            trump_me_count += 1

    print('TRUMP: ')
    trump_superlative_percentage = 100 * trump_superlative_count / len(trump_words)
    print('Superlative percentage: ', trump_superlative_percentage)
    trump_me_percentage = 100 * trump_me_count / len(trump_words)
    print('Me percentage: ', trump_me_percentage)
    trump_black_and_white_percentage = 100 * trump_black_and_white_count / len(trump_words)
    print('Good/bad percentage: ', trump_black_and_white_percentage)

    lowercase_letters = [chr(c) for c in range(ord('a'), ord('z') + 1)]
    uppercase_letters = [chr(c) for c in range(ord('A'), ord('Z') + 1)]

    # remove non-words
    for word in trump_words:
        for c in word:
            if c not in lowercase_letters and c not in uppercase_letters:
                if len(word) == 1:
                    trump_words.remove(word)

    for word in clinton_words:
        for c in word:
            if c not in lowercase_letters and c not in uppercase_letters:
                if len(word) == 1:
                    clinton_words.remove(word)

    clinton_superlative_count = 0
    clinton_me_count = 0
    clinton_black_and_white_count = 0

    # find consecutive words
    for i in range(len(clinton_words) - 1):
        current = clinton_words[i]
        if current in superlatives:
            clinton_superlative_count += 1
        if current in black_and_white:
            clinton_black_and_white_count += 1
        if 'I' in current or current == 'me':
            clinton_me_count += 1

    print('CLINTON: ')
    clinton_superlative_percentage = 100 * clinton_superlative_count / len(clinton_words)
    print('Superlative percentage: ', clinton_superlative_percentage)
    clinton_me_percentage = 100 * clinton_me_count / len(clinton_words)
    print('Me percentage: ', clinton_me_percentage)
    clinton_black_and_white_percentage = 100 * clinton_black_and_white_count / len(clinton_words)
    print('Good/bad percentage: ', clinton_black_and_white_percentage)

    print('Trump has ' + str(len(trump_words)) + ' words')
    print('Clinton has ' + str(len(clinton_words)) + ' words')

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

    interesting_words = ['they','very','because','what','think','would', 'be', 'great', 'bad', 'worst']
    for word in interesting_words:
        print(word.upper())
        print('Trump frequency: ' + str(trump_dictionary[word]))
        print('Trump percentage: ' + str(round(100 * trump_dictionary[word] / len(trump_words), 2)) + '%')
        print('Clinton frequency: ' + str(clinton_dictionary[word]))
        print('Clinton percentage: ' + str(round(100 * clinton_dictionary[word] / len(clinton_words), 2)) + '%')

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

    print(clinton_dictionary)
    #create_frequent_histogram(trump_dictionary, 50, 'Most frequent words used by Trump in first debate')

    create_frequent_histogram(clinton_dictionary, 37, 'Most frequent words used by Clinton in first debate')



    for word in clinton_words:
        if word in clinton_dictionary:
            clinton_dictionary[word] += 1
        else:
            clinton_dictionary[word] = 1

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


def get_words_from_lines(lines):
    global special_words

    all_words = []
    for line in lines:
        words = line.split(' ')
        for word in words:
            if not word:
                words.remove(word)
        for i in range(len(words)):
            # found word with trailing punctuation
            if '.' in words[i] or '?' in words[i]:
                # check if next word is proper noun. if not, make lowercase
                if i + 1 < len(words):
                    next_word = words[i + 1]
                    if 'A' <= next_word[0] <= 'Z' and re.sub(r'[.,?"]', '', next_word) not in special_words:
                        # print('Next word after punctuation is: ' + next_word)
                        # print('Changed to: ' + words[i+1])
                        words[i + 1] = words[i + 1].lower()
            words[i] = re.sub(r'[.;,?"]', '', words[i])
        for word in words:
            if not word:
                words.remove(word)
                # if word[0] >= 'A' and word[0] <= 'Z' and word not in special_words:
                #  print('Found capitalized word: ' + word)
        first_word = words[0]
        if 'A' <= first_word[0] <= 'Z' and first_word not in special_words:
            words[0] = words[0].lower()
        for word in words:
          all_words.append(word)
    return all_words



def create_frequent_histogram(dictionary, min_occurrences, title):

    frequent_dictionary = {}
    for word in dictionary:
      if dictionary[word] > min_occurrences:
        frequent_dictionary[word] = dictionary[word]

    sorted_values = sorted(frequent_dictionary.values())
    sorted_keys = sorted(frequent_dictionary, key=frequent_dictionary.get)

    sorted_keys.reverse()
    sorted_values.reverse()

    indexes = np.arange(len(sorted_keys))
    plt.bar(indexes, sorted_values)
    plt.xticks(indexes + 0.3, sorted_keys)
    plt.xlabel('Word')
    plt.ylabel('Frequency')
    plt.title(title)

    plt.show()



main()
