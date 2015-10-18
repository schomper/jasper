#! /usr/bin/python3

# ------------------------------------------------------------------------------
# Name: gen_sub_topics.py
#
# Usage: Using the gamma file and the format file this script produces a format
#        file for each one of the sub topics. This is based of a tolerance
#        value which if the gamma number is below that document is not part of
#        said topic
# ------------------------------------------------------------------------------

import sys


def write_line(pointer, index, probability, line):
    pointer.write(index + '|~|' + probability + '|~|' + line + '\n')


def lowest_topics(probability, utility, pointer, line, index):
    if probability > utility:
        write_line(pointer, index, probability, line)


def highest_val_index(unsorted_list):
    max_index = 0
    max_value = float(unsorted_list[0])

    for index in range(len(unsorted_list)):
        if float(unsorted_list[index]) > max_value:
            max_value = float(unsorted_list[index])
            max_index = index

    return max_index


def write_files(format_file, gamma_file, run_type, utility):
    output_files = []
    num_topics = 0

    with open(format_file) as data_file:
        format_lines = data_file.readlines()

    with open(gamma_file) as data_file:
        gamma_lines = data_file.readlines()

    for topic_index in range(gamma_lines[0].split(' ')):
        file_ptr = open('sub_' + str(topic_index) + '.txt', 'w')
        output_files.append(file_ptr)

    for index in range(len(format_lines)):
        format_line = format_lines[index].strip()
        gamma_line = gamma_lines[index].strip()

        topic_values = gamma_line.split(' ')

        if run_type == 'highest':
            max_index = highest_val_index(topic_values)
            write_line(topic_values[max_index], index,
                       topic_values[max_index], format_line)

        if run_type == 'lowest':
            for x in range(len(topic_values)):
                lowest_topics(topic_values[x], utility, output_files[x],
                              format_line, index)

    return num_topics


def reindex_files(directory, index):
    original_vocab = []
    new_vocab = []

    vocab_file = directory + '/initial.vocab'
    format_file = directory + '/initial.formatted'
    group_name = directory + '/' + index + '/'

    with open(vocab_file, 'r') as vocab_ptr:
        original_vocab = vocab_ptr.readlines()

    for index in range(0, len(original_vocab)):
        original_vocab[index] = original_vocab[index].strip()

    vocab_out_ptr = open(group_name + 'initial.vocab', 'w')
    format_out_ptr = open(group_name + 'initial.formatted', 'w')

    with open(format_file, 'r') as format_ptr:
        lines = format_ptr.readlines()

    for line in lines:
        line = line.strip()

        meta, pair_list = line.rsplit('|~|', 1)
        pair_list = pair_list.split(' ')
        num_pairs = pair_list.pop(0)

        format_out_ptr.write(meta + '|~|')
        format_out_ptr.write(num_pairs)

        for pair in pair_list:
            word_index, word_count = pair.split(':')

            word = original_vocab[int(word_index)]

            if word not in new_vocab:
                new_vocab.append(word)
                vocab_out_ptr.write(word + '\n')

            index = new_vocab.index(word)
            format_out_ptr.write(' %d:%d' % (index, int(word_count)))

        format_out_ptr.write('\n')


def main():
    if len(sys.argv) != 4:
        print('./generate_sub_topics.py <input_directory> ' +
              '<lowest/confidence/highest> <utility>')
        exit(1)

    input_directory = sys.argv[1]
    num_sub_topics = int(sys.argv[2])
    run_type = sys.argv[3]
    utility = float(sys.argv[4])

    format_file = input_directory + '/initial.formatted'
    gamma_file = input_directory + '/out/final.gamma'

    num_topics = write_files(format_file, gamma_file, num_sub_topics,
                             run_type, utility)

    for index in range(num_topics):
        reindex_files(input_directory, str(index))


if __name__ == '__main__':
    main()
