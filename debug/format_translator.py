#! /usr/bin/python3

import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

input_ptr = open(input_file, 'r')
output_ptr = open(output_file, 'w')

line = input_ptr.readline()

while line != '':
    junk, stuff = line.rsplit('|~|', 1)
    
    output_ptr.write(stuff)
    line = input_ptr.readline()
    
input_ptr.close()
output_ptr.close()
