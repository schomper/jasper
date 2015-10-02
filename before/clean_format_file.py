#! /usr/bin/python3
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('./clean_format_file.py <dirty_format> <output_file>')

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
