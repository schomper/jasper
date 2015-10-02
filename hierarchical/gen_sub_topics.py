#! /usr/bin/python3

import sys

def main():
    if len(sys.argv) != 6:
        print('./gen_sub_topics.py <gamma_file> <format_file> <lowest_significant> <num_topics> <output_string>')
        exit(1)

    gamma_file = sys.argv[1]
    format_file = sys.argv[2]
    lowest = float(sys.argv[3])
    num_topics = int(sys.argv[4])
    output_string = sys.argv[5]

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

        for x in range(0, len(topics)):
            if float(topics[x]) > lowest:
                output_files[x].write(str(count) + '|~|' + topics[x] + '|~|' + format_line + '\n')

        count += 1
        format_line = format_ptr.readline()
        gamma_line = gamma_ptr.readline()

if __name__ == '__main__':
    main()
