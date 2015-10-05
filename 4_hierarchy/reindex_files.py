#! /usr/bin/python3
import sys

# ------------------------------------------------------------------------------
# Name: reindex_files.py
#
# Usage: reindexes the format and vocab files after a hierarchy split has
#        occured. This is achieved through creating two new files which
#        represent the vocab appropriately
# ------------------------------------------------------------------------------


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('reindex_files.py <format_file> <vocab_file> <group_name>')
        exit(1)

    format_file = sys.argv[1]
    vocab_file = sys.argv[2]
    group_name = sys.argv[3]

    original_vocab = []
    new_vocab = []

    with open(vocab_file, 'r') as vocab_ptr:
        original_vocab = vocab_ptr.readlines()

    for index in range(0, len(original_vocab)):
        original_vocab[index] = original_vocab[index].strip()

    vocab_out_ptr = open(group_name + '.vocab', 'w')
    format_out_ptr = open(group_name + '.formatted', 'w')

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
