#! /usr/bin/python3
import re
import sys
import json
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


def clean_line(line):
    stemmer = SnowballStemmer('english')
    new_words = []
    
    # remove digits
    clean_line = ''.join([index for index in line if not index.isdigit()])

    # make words lowercase
    clean_line = clean_line.lower()
    words_list = clean_line.split(' ')

    #print(words_list)
    for word in words_list:
        word = word.strip(' ')

        # remove stop words
        if word in stopwords.words('english'):
            continue

        word = re.sub(r'\s+', "", word)
        if word == '':
            continue

        word = stemmer.stem(word)
        new_words.append(word)

    clean_line = ' '.join(new_words)

    return clean_line


def classify(document_contents, vocab_details, vocab_index):
    document_hash = {}

    document_words = document_contents.split(' ')

    for word in document_words:
        if word == '':
            continue

        if word not in vocab_index:
            print('Word is unknown: %s' % word)
            continue

        else:
            word_index = str(vocab_index[word])
            word_total = vocab_details[word_index]['total']
            word_topics = vocab_details[word_index]['topics']

            for topic in word_topics:
                if topic not in document_hash:
                    document_hash[topic] = 0

                document_hash[topic] += \
                    vocab_details[word_index]['topics'][topic] / word_total

    topics = []
    for key in document_hash:
        topics.append(document_hash[key])

    indices = list(range(len(topics)))
    indices = sorted(indices, key=lambda x: -topics[x])

    return indices


def compare_top(classed_topics, known_topics):
    #print('\n')
    #print(str(classed_topics))
    #print('\t' + str(known_topics))
    if str(classed_topics[0]) == str(known_topics[0]):
        return True
    else:
        return False


def main():
    top_count = 0
    top_three_count = 0
    order_count = 0

    if len(sys.argv) != 3:
        print('./test_doc_guess_algorithm.py <folder> <output>')
        exit(1)

    # Input naming
    folder = sys.argv[1]
    output = sys.argv[2]

    # File allocation
    format_file = folder + '/initial.formatted'
    vocab_details_file = folder + '/vocab_details.json'
    vocab_index_file = folder + '/vocab_index.json'
    document_topics_file = folder + '/doc_topics.txt'

    # Read in required data
    with open(vocab_details_file) as data_file:
        vocab_details = json.load(data_file)

    with open(vocab_index_file) as data_file:
        vocab_index = json.load(data_file)

    with open(format_file) as data_file:
        format_lines = data_file.readlines()

    with open(document_topics_file) as data_file:
        topic_lines = data_file.readlines()

    num_docs = len(format_lines)

    for index in range(len(format_lines)):
        line = format_lines[index]
        line = line.strip()

        if index % 1000 == 0:
            print(str(index))
        known_topics = topic_lines[index].strip().split(' ')
        document_contents = line.split('|~|')[3]
        document_contents = clean_line(document_contents)
        classed_doc = classify(document_contents, vocab_details, vocab_index)
        #print(str(classed_doc))
        # Compare the classification against the known
        if compare_top(classed_doc, known_topics):
            top_count += 1
        # compare_top_three(classified_doc)
        # compare_order(classified_doc)

    print('Top Correct: ' + str(top_count / num_docs))

if __name__ == '__main__':
    main()
