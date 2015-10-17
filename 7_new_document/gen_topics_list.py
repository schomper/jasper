#! /usr/bin/python3
import sys


def main():
    if len(sys.argv) != 3:
        print('./gen_topics_list.py <gamma_file> <output>')
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    output_ptr = open(output_file, 'w')

    with open(input_file) as data_file:
        topic_lines = data_file.readlines()

    for line in topic_lines:
        line = line.strip()
        topics = [float(x) for x in line.split()]
        indices = list(range(len(topics)))
        indices = sorted(indices, key=lambda x: -topics[x])


        line = ' '.join(map(str, indices))
        output_ptr.write(line + '\n')

    output_ptr.close()

if __name__ == '__main__':
    main()