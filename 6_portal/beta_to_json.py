#! /usr/bin/python3
import sys
import json


def main():
    overall_array = []
    overall_dict = {}

    if len(sys.argv) != 2:
        print('./beta_to_json <gamma_file>')
        exit(1)

    file_name = sys.argv[1]

    file_ptr = open(file_name, 'r')

    line = file_ptr.readline()

    count = 0

    topics = {}
    word_likelihood = []

    # Process lines
    while line != '':
        line = line.strip()

        word_likelihood = line.split(' ')
        topics[count] = word_likelihood

        line = file_ptr.readline()
        count += 1

    overall_dict['NumTopics'] = count
    overall_dict['Topics'] = topics

    # write json out
    output_ptr = open('topic_to_word.json', 'w')
    output_ptr.write(json.dumps(overall_array, sort_keys=True, indent=4))
    output_ptr.close()

if __name__ == '__main__':
    main()
