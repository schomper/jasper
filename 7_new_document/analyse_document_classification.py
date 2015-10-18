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

    keys = []
    for key in document_hash:
        keys.append(key)
    keys.sort()

    topics = list(range(len(keys)))
    for index in range(len(keys)):
        topics[index] = document_hash[keys[index]]

    indices = list(range(len(topics)))
    indices = sorted(indices, key=lambda x: -topics[x])

    return indices


def compare_topics_order(classed, known, amount):
    """ (list, list, int) -> boolean

    Returns true the number of elements in amount are in the correct order
    """
    correct = True

    for index in range(amount):
        if str(classed[index]) != str(known[index]):
            correct = False
            break

    return correct


def compare_topic_slice(classed, known, cutoff):
    """ (list, list, int) -> boolean

    Returns true if both lists contain the same items up to the cutoff
    """

    classed = classed[:cutoff]
    known = known[:cutoff]

    known.sort()
    classed.sort()

    for i in range(cutoff):
        if i == len(known):
            break
        if i == len(classed):
            break
        if str(known[i]) != str(classed[i]):
            return False

    return True


def compare_position_offset(classed, known, offset):
    """ (list, list, int) -> boolean

    Returns true if the elements within the list
    are never more than offset positions away from each other
    """
    num_topics = len(classed)

    for index in range(num_topics):
        correct = False

        for i in range(offset):
            plus = index + i
            minus = index - i

            if not minus < 0:
                if(str(classed[index]) == str(known[minus])):
                    correct = True
                    break

            if not plus >= len(range(known)):
                if(str(classed[index]) == str(known[plus])):
                    correct = True
                    break

        if not correct:
            return False

    return True


def main():
    check_start('./test_doc_guess_algorithm.py <folder> <output>', 3)
    topic_order_count = 0
    topic_feeling_count = 0
    topic_offset_count = 0

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

        if len(classed_doc) == 0:
            print(document_contents)
            continue

        if compare_topics_order(classed_doc, known_topics, 1):
            topic_order_count += 1

        if compare_topic_slice(classed_doc, known_topics, 3):
            topic_feeling_count += 1

        if compare_position_offset(classed_doc, known_topics, 1):
            topic_offset_count += 1

        if index % 100 == 0:
            print(str(index))

    out_ptr = open(output, 'w')
    out_ptr.write('Number of documents: ' + str(num_docs) + '\n')
    out_ptr.write('Topics Correct: %s\n' % str(topic_order_count / num_docs))

    print('Number of documents: ' + str(num_docs))
    print('Topics Correct: ' + str(topic_order_count / num_docs))
    print('Topics Kinda Right: ' + str(topic_feeling_count / num_docs))
    print('Topics offset Right: ' + str(topic_offset_count  / num_docs))
    print('\a')

if __name__ == '__main__':
    main()
