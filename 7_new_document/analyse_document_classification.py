#! /usr/bin/python3
import sys
import json
from utils import clean_line, check_start


def classify(contents, vocab_details, vocab_index):
    """ (str, dict, dict) -> list

    Return the document's topics in order of relevance
    """
    topics = []
    document_hash = {}

    document_words = contents.split(' ')

    for word in document_words:
        assert word != ''
        assert word in vocab_index

        word_index = str(vocab_index[word])
        word_total = vocab_details[word_index]['total']
        word_topics = vocab_details[word_index]['topics']

        for topic in word_topics:
            if topic not in document_hash:
                document_hash[topic] = 0

            document_hash[topic] += \
                vocab_details[word_index]['topics'][topic] / word_total

    for key in document_hash:
        topics.append(document_hash[key])

    indices = list(range(len(topics)))
    indices = sorted(indices, key=lambda x: -topics[x])

    return indices


def compare_topics(classed, known, amount):
    """ (list, list, int) -> boolean

    Returns true the number of elements in amount are in the correct order
    """
    correct = True

    for index in range(amount):
        if str(classed[index]) != str(known[index]):
            correct = False
            break

    return correct


def main():
    check_start('./test_doc_guess_algorithm.py <folder> <output>', 3)
    top_count = 0

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

        known_topics = topic_lines[index].strip().split(' ')
        document_contents = line.split('|~|')[3]
        document_contents = clean_line(document_contents)
        classed_doc = classify(document_contents, vocab_details, vocab_index)

        if compare_topics(classed_doc, known_topics, 1):
            top_count = 1 + top_count

    print('Topics Correct: ' + str(top_count / num_docs))

if __name__ == '__main__':
    main()
