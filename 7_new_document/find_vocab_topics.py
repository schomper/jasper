#! /usr/bin/python3

import sys
import json
# ------------------------------------------------------------------------------
# Name: find_vocab_topics.py
#
# Usage: Creates a json hash files which has the word index as key and
#        information about how often the word appears and in what context
# ------------------------------------------------------------------------------


def main():

    if len(sys.argv) != 4:
        print('./find_vocab_topics.py <vocab_file>  \
            <word_assignment_file> <output_file>')
        exit(1)

    vocab_file = sys.argv[1]
    word_assignment_file = sys.argv[2]
    output_file = sys.argv[3]

    overall_hash = {}
    vocab_index = 0

    vocab_ptr = open(vocab_file, 'r')
    line = vocab_ptr.readline()

    # Process each line of the vocab file
    while line != '':
        word_hash = {}

        line = line.strip()

        word_hash['word'] = line
        word_hash['topics'] = {}
        word_hash['total'] = 0
        overall_hash[vocab_index] = word_hash

        line = vocab_ptr.readline()
        vocab_index += 1

    vocab_ptr.close()

    word_assignment_ptr = open(word_assignment_file, 'r')
    line = word_assignment_ptr.readline()

    # process each line of the word assignment file
    while line != '':
        line = line.strip()

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

        line = word_assignment_ptr.readline()

    word_assignment_ptr.close()

    output_ptr = open(output_file, 'w')
    output_ptr.write(json.dumps(overall_hash, sort_keys=True, indent=4))
    output_ptr.close()


if __name__ == '__main__':
    main()
