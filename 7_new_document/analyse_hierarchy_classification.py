#! /usr/bin/python3
import sys
import os
from utils import check_start, clean_line

TOTAL_TOPICS = 0
NUM_TOP_TOPICS = 0
NUM_SUB_TOPICS = 0


def classify(contents, weights, word_dict):
    global NUM_SUB_TOPICS
    global NUM_TOP_TOPICS

    document_topics = {}

    for i in range(NUM_TOP_TOPICS):
        document_topics[i] = [0] * NUM_SUB_TOPICS

    words = contents.split(' ')

    for word in words:

        if word not in word_dict:
            continue

        for topic in word_dict[word]:
            if topic == 'total':
                continue

            for sub_topic in word_dict[word][topic]:

                value = (word_dict[word][topic][sub_topic] /
                         word_dict[word]['total']) * weights[topic]

                document_topics[topic][sub_topic] += value

    return document_topics


def get_document_values(index, hierarchy_struct):
    """ (int, dict) -> list

    Returns an array with the weighting of a topic to be attributed
    to the document words
    """
    weighting = [0] * len(hierarchy_struct)

    total = 0
    for dict_index in range(len(hierarchy_struct)):
        if index in hierarchy_struct[dict_index]:
            weighting[dict_index] =\
                    hierarchy_struct[dict_index][index]
            total += weighting[dict_index]

    for index in range(len(weighting)):
        weighting[index] = weighting[index]/total

    return weighting


def get_word_dictionary(folder, vocab_file):

    # TODO possibly additional weighting
    # based of high level word file
    word_dictionary = {}

    # Read in required data
    with open(vocab_file) as data_file:
        vocab_lines = data_file.readlines()

    for index in range(len(vocab_lines)):
        line = vocab_lines[index].strip()
        word_dictionary[line] = {}
        word_dictionary[line]['total'] = 0

    # ----------------- Process each sub-topic directory ----------------- #
    files_list = os.listdir(folder)
    for item in files_list:
        index_to_word = {}
        if not item.isdigit():
            continue

        topic_number = int(item)
        topic_folder = folder + '/' + item
        topic_vocab_file = topic_folder + '/initial.vocab'
        topic_word_ass_file = topic_folder + '/out/word-assignments.dat'

        with open(topic_word_ass_file) as data_file:
            word_ass_lines = data_file.readlines()

        with open(topic_vocab_file) as data_file:
            topic_vocab_lines = data_file.readlines()

        # Get index for words in this vocab to be able to get word in dict
        for index in range(len(topic_vocab_lines)):
            line = topic_vocab_lines[index].strip()
            index_to_word[index] = line

        for line in word_ass_lines:
            line = line.strip()
            tokens = line.split(' ')

            tokens.pop(0)
            for token in tokens:
                word_index, topic_index = token.split(':')
                word = index_to_word[int(word_index)]

                if topic_number not in word_dictionary[word]:
                    word_dictionary[word][topic_number] = {}

                if int(topic_index) not in word_dictionary[word][topic_number]:
                    word_dictionary[word][topic_number][int(topic_index)] = 0

                word_dictionary[word][topic_number][int(topic_index)] += 1
                word_dictionary[word]['total'] += 1

    return word_dictionary


def get_hierarchy_struct(folder):
    global NUM_SUB_TOPICS

    files_list = os.listdir(folder)
    hierarchy_struct = [{}] * len(files_list)

    for i in range(len(files_list)):
        item = files_list[i]

        if not item.isdigit():
            continue

        topic_folder = folder + '/' + item
        format_file = topic_folder + '/initial.formatted'
        info_file = topic_folder + '/out/final.other'

        with open(format_file) as data_file:
            format_lines = data_file.readlines()

        with open(info_file) as data_file:
            info_lines = data_file.readlines()

        NUM_SUB_TOPICS = int(info_lines[0].split(' ')[1])

        for line in format_lines:
            line = line.strip()
            parts = line.split('|~|')

            index = int(parts[0])
            value = float(parts[1])

            hierarchy_struct[i][index] = value

    return hierarchy_struct


def get_known_topics(folder):
    known_topics = []
    big_dict = {}

    files_list = os.listdir(folder)

    for i in range(len(files_list)):
        item = files_list[i]

        if not item.isdigit():
            continue

        gamma_file = folder + '/' + str(item) + '/out/final.gamma'
        format_file = folder + '/' + str(item) + '/initial.formatted'

        with open(format_file) as data_file:
            format_lines = data_file.readlines()

        with open(gamma_file) as data_file:
            gamma_lines = data_file.readlines()

        for index in range(len(format_lines)):
            gamma_line = gamma_lines[index].strip()
            doc_index = int(format_lines[index].split('|~|')[0])

            if doc_index not in big_dict:
                big_dict[doc_index] = {}

            big_dict[doc_index][item] = []

            tokens = gamma_line.split(' ')

            for topic in tokens:
                big_dict[doc_index][item].append(float(topic))

    known_topics = [''] * len(big_dict)

    for index in big_dict:
        if index == 0:
            print(str(big_dict[index]))
        known_topics[index] = get_classed_array(big_dict[index])

    return known_topics


def get_highest(classed):
    highest_topic = 0
    highest_sub_topic = 0
    highest_value = 0

    # Find highest
    for topic in classed:
        for i in range(len(classed[topic])):
            if classed[topic][i] > highest_value:
                highest_value = classed[topic][i]
                highest_topic = topic
                highest_sub_topic = i

    classed[highest_topic][highest_sub_topic] = 0

    topics_to_remove = []
    for topic in classed:
        all_zero = True
        for i in classed[topic]:
            if i != 0:
                all_zero = False
                break

        if all_zero:
            topics_to_remove.append(topic)

    for topic in topics_to_remove:
        classed.pop(topic, None)

    highest = str(highest_topic) + ':' + str(highest_sub_topic)
    return [highest, classed]


def get_classed_array(classed):
    classed_array = []

    elements_left = True
    while elements_left:
        highest, classed = get_highest(classed)
        classed_array.append(highest)

        if classed == {}:
            elements_left = False

    return classed_array


def compare_topics_order(classed, known, amount):
    """ (list, list, int) -> boolean

    Returns true the number of elements in amount are in the correct order
    """
    for index in range(amount):
        if str(classed[index]) != str(known[index]):
            return False

    return True


def main():
    global NUM_TOP_TOPICS

    check_start('./test_doc_guess_algorithm.py <folder> ' +
                '<output> <num_topics>', 4)

    # Input naming
    folder = sys.argv[1]
    output = sys.argv[2]
    num_topics = int(sys.argv[3])

    topic_order_count = 0
    topic_feeling_count = 0
    topic_offset_count = 0

    # File allocation
    format_file = folder + '/initial.formatted'
    vocab_file = folder + '/initial.vocab'
    info_file = folder + '/out/final.other'

    with open(format_file) as data_file:
        format_lines = data_file.readlines()

    with open(info_file) as data_file:
            info_lines = data_file.readlines()

    NUM_TOP_TOPICS = int(info_lines[0].split(' ')[1])

    known_topics = get_known_topics(folder)
    print(str(known_topics[0]))
    word_dict = get_word_dictionary(folder, vocab_file)
    hierarchy_struct = get_hierarchy_struct(folder)

    # Cycle through top-level documents
    count = 0
    for index in range(len(format_lines)):
        line = format_lines[index]
        line = line.strip()

        # known_topics = get_known_topics()

        weights = get_document_values(index, hierarchy_struct)
        contents = line.split('|~|')[3]
        contents = clean_line(contents)
        classed_doc = classify(contents, weights, word_dict)
        classed_array = get_classed_array(classed_doc)

        if index % 1000 == 0 and index != 0:
            print('\tTopics correct position ' +
                  '%d: %s' % (index, str(topic_order_count / index)))

        if compare_topics_order(classed_array, known_topics[index], 1):
            topic_order_count += 1

        count += 1

    print('\tTopics correct position %d: %s' % (count, str(topic_order_count / count)))

if __name__ == '__main__':
    main()
