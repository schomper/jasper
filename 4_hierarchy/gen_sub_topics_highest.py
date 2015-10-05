#! /usr/bin/python3

# ------------------------------------------------------------------------------
# Name: gen_sub_topics.py
#
# Usage: Using the gamma file and the format file this script produces a format
#        file for each one of the sub topics. This is based purely of the
#        highest value topic for a document
# ------------------------------------------------------------------------------

import sys


def highest_val_index(unsorted_list):
    max_index = 0
    max_value = float(unsorted_list[0])

    for index in range(len(unsorted_list)):
        if float(unsorted_list[index]) > max_value:
            max_value = float(unsorted_list[index])
            max_index = index

    return max_index


def main():
    if len(sys.argv) != 5:
        print('./gen_sub_topics_highest.py <gamma_file> <format_file> ' +
              '<num_topics> <output_string>')
        exit(1)

    gamma_file = sys.argv[1]
    format_file = sys.argv[2]
    num_topics = int(sys.argv[3])
    output_string = sys.argv[4]

    output_files = []

    for x in range(0, num_topics):
        file_ptr = open(output_string + str(x) + '.txt', 'w')
        output_files.append(file_ptr)

    format_ptr = open(format_file, 'r')
    gamma_ptr = open(gamma_file, 'r')

    format_line = format_ptr.readline()
    gamma_line = gamma_ptr.readline()
    count = 0

    while format_line != '':
        format_line = format_line.strip()
        gamma_line = gamma_line.strip()

        topics = gamma_line.split(' ')
        max_index = highest_val_index(topics)

        output_files[max_index].write(str(count) + '|~|' + topics[max_index]
                                                 + '|~|' + format_line + '\n')

        count += 1
        format_line = format_ptr.readline()
        gamma_line = gamma_ptr.readline()

if __name__ == '__main__':
    main()
