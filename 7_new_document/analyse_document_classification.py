#! /usr/bin/python3
import sys
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

        if word not in vocab_index:
            continue

        word_index = vocab_index[word]
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
    for index in range(amount):
        if str(classed[index]) != str(known[index]):
            return False

    return True


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

            if not plus >= len(known):
                if(str(classed[index]) == str(known[plus])):
                    correct = True
                    break

        if not correct:
            return False

    return True


def get_vocab_details(vocab_lines, word_assignment_lines):
    overall_hash = {}

    # Process each line of the vocab file
    for index in range(len(vocab_lines)):
        word_hash = {}

        line = vocab_lines[index].strip()

        word_hash['word'] = line
        word_hash['topics'] = {}
        word_hash['total'] = 0
        overall_hash[index] = word_hash

    # process each line of the word assignment file
    for index in range(len(word_assignment_lines)):
        line = word_assignment_lines[index].strip()

        word_topics = line.split(' ')
        word_topics.pop(0)               # remove word amount

        for word_topic in word_topics:
            word_index, topic_index = word_topic.split(':')

            word_index = int(word_index)

            if word_index not in overall_hash:
                print('overall hash does not contain \
                       this word index %d' % word_index)
                exit(1)

            if topic_index in overall_hash[word_index]['topics']:
                overall_hash[word_index]['topics'][topic_index] += 1
            else:
                overall_hash[word_index]['topics'][topic_index] = 1

            overall_hash[word_index]['total'] += 1

    return overall_hash


def get_vocab_index(vocab_lines):
    overall_hash = {}

    for index in range(len(vocab_lines)):
        line = vocab_lines[index].strip()
        overall_hash[line] = index

    return overall_hash


def get_document_topics(gamma_lines):
    return_list = []

    for line in gamma_lines:
        line = line.strip()
        topics = [float(x) for x in line.split()]
        indices = list(range(len(topics)))
        indices = sorted(indices, key=lambda x: -topics[x])

        line = ' '.join(map(str, indices))
        return_list.append(line)

    return return_list


def main():
    check_start('./test_doc_guess_algorithm.py <folder> <output> <num_topics>', 4)

    # Input naming
    folder = sys.argv[1]
    output = sys.argv[2]
    num_topics = int(sys.argv[3])

    topic_order_count = [0] * num_topics
    topic_feeling_count = [0] * num_topics
    topic_offset_count = [0] * num_topics

    # File allocation
    format_file = folder + '/initial.formatted'
    vocab_file = folder + '/initial.vocab'
    word_assignment_file = folder + '/out/word-assignments.dat'
    gamma_file = folder + '/out/final.gamma'

    # Read in required data
    with open(vocab_file) as data_file:
        vocab_lines = data_file.readlines()

    with open(word_assignment_file) as data_file:
        word_assignment_lines = data_file.readlines()

    with open(format_file) as data_file:
        format_lines = data_file.readlines()

    with open(gamma_file) as data_file:
        gamma_lines = data_file.readlines()

    vocab_details = get_vocab_details(vocab_lines, word_assignment_lines)
    topic_lines = get_document_topics(gamma_lines)
    vocab_index = get_vocab_index(vocab_lines)

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

        if index % 1000 == 0 and index != 0:
            print('Snapshot: ' + str(index))
            for i in range(1, num_topics):
                print('\tTopics correct position %d: %s' % (i, str(topic_order_count[i] / index)))
                print('\tTopics within range %d: %s' % (i, str(topic_feeling_count[i] / index)))
                print('\tTopics within offset %d: %s' % (i, str(topic_offset_count[i] / index)))

        for i in range(1, len(classed_doc)):
            if compare_topics_order(classed_doc, known_topics, i):
                topic_order_count[i] += 1

            if compare_topic_slice(classed_doc, known_topics, i):
                topic_feeling_count[i] += 1

            if compare_position_offset(classed_doc, known_topics, i):
                topic_offset_count[i] += 1

    out_ptr = open(output, 'w')

    out_ptr.write('Number of documents: ' + str(num_docs) + '\n')
    for i in range(num_topics):
        out_ptr.write('Topics correct position %d: %s\n' % (i, str(topic_order_count[i] / num_docs)))
        out_ptr.write('Topics within range %d: %s\n' % (i, str(topic_feeling_count[i] / num_docs)))
        out_ptr.write('Topics within offset %d: %s\n' % (i, str(topic_offset_count[i] / num_docs)))

if __name__ == '__main__':
    main()
