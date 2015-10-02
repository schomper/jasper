#! /usr/bin/python3
import sys

# ----------------------------------------------------------------------------
# Name: items_per_line
#
# Usage: items_per_line counts the amount of space speparated tokens there are
#        in each line of a file. Printing the tokens in the line and the amount
#        of items in that line.
#
# ----------------------------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('./items_per_line.py <file>')

    file = sys.argv[1]

    with open(file, 'r') as file_ptr:
        lines = file_ptr.readlines()

    count = 1

    for line in lines:
        line = line.strip()
        tokens = line.split(' ')

        print('line %d has %d tokens' % (count, len(tokens)))
        print('    ' + str(tokens))

        count += 1
