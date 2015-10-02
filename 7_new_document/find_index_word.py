#! /usr/bin/python3

# ------------------------------------------------------------------------------
# Name: find_index_word.py
#
# Usage: Creates a hash with each word in the vocab being a key for its index
# ------------------------------------------------------------------------------
import sys
import json


def main():

    if len(sys.argv) != 3:
        print('./find_vocab_topics.py <vocab_file> <output_file>')
        exit(1)

    vocab_file = sys.argv[1]
    output_file = sys.argv[2]

    overall_hash = {}

    vocab_index = 0

    vocab_ptr = open(vocab_file, 'r')
    line = vocab_ptr.readline()

    # Process each line of the vocab file
    while line != '':

        line = line.strip()

        overall_hash[line] = vocab_index

        line = vocab_ptr.readline()
        vocab_index += 1

    vocab_ptr.close()

    output_ptr = open(output_file, 'w')
    output_ptr.write(json.dumps(overall_hash, sort_keys=True, indent=4))
    output_ptr.close()


if __name__ == '__main__':
    main()
