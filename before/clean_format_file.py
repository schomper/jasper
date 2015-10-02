#! /usr/bin/python3

# ------------------------------------------------------------------------------
# Name: clean_format_file.py
# 
# Usage: script takes a format file and turns it into a format file that is
# usable by the C lda script
# ------------------------------------------------------------------------------
import sys


def main():
    if len(sys.argv) != 3:
        print('./clean_format_file.py <original_format> <c_lda_format>')

    format_file = sys.argv[1]
    output_file = sys.argv[2]

    format_ptr = open(format_file, 'r')
    output_ptr = open(output_file, 'w')

    line = format_ptr.readline()

    while line != '':
        line = line.strip()

        front, back = line.rsplit('|~|', 1)
        if back != '0':
            output_ptr.write(line + '\n')

        line = format_ptr.readline()

    format_ptr.close()
    output_ptr.close()

if __name__ == '__main__':
    main()
