#! /usr/bin/python3
# ------------------------------------------------------------------------------
# Name: guess_new_document.py
#
# Usage: Guess the topics of a new document by adding together the frequencies
# and relationships of its words
# ------------------------------------------------------------------------------
import sys
import json
from utils import clean_line, check_start


def main():
    check_start('guess_new_document.py <document> <vocab_file> ' +
                '<vocab_details_file> <output_file>', 5)

    document_file = sys.argv[1]
    vocab_file = sys.argv[2]
    vocab_details_file = sys.argv[3]
    output_file = sys.argv[4]

    document_hash = {}

    with open(vocab_file) as data_file:
        vocab_index_data = json.load(data_file)

    with open(vocab_details_file) as data_file:
        vocab_details_data = json.load(data_file)

    document_ptr = open(document_file, 'r')

    line = document_ptr.readline()

    while line != '':
        line = line.strip()
        line = clean_line(line)

        words = line.split(' ')

        for word in words:
            if word == '':
                continue

            # TODO there is a bug here
            if word not in vocab_index_data:
                print('Word is unknown: %s' % word)

            else:
                word_index = str(vocab_index_data[word])
                word_total = vocab_details_data[word_index]['total']
                word_topics = vocab_details_data[word_index]['topics']

                for word_topic in word_topics:

                    if word_topic not in document_hash:
                        print('Adding topic %s' % word_topic)
                        document_hash[word_topic] = 0

                    document_hash[word_topic] += vocab_details_data[
                                word_index]['topics'][word_topic] / word_total

        line = document_ptr.readline()

    document_ptr.close()

    output_ptr = open(output_file, 'w')
    output_ptr.write(json.dumps(document_hash, sort_keys=True, indent=4))
    output_ptr.close()


if __name__ == "__main__":
    main()
