#! /usr/bin/python3
import sys
import json

def main():
    
    overall_array = []
    overall_dict = {}

    if len(sys.argv) != 2:
        print('./gamma_to_json <gamma_file>');    
        exit(1)

    file_name = sys.argv[1]
    
    file_ptr = open(file_name, 'r')

    line = file_ptr.readline()

    count = 0
    
    documents = {}
    topic_likelihood = []

    # Process lines
    while line != '':
        line = line.strip()
        
        topic_likelihood = line.split(' ')
        
        documents[count] = topic_likelihood

        line = file_ptr.readline()
        count += 1
        
    
    overall_dict['NumDocuments'] = count
    overall_dict['Documents'] = documents

    # write json out
    output_ptr = open('document_to_topic.json', 'w')
    output_ptr.write(json.dumps(overall_dict, sort_keys=True, indent=4))
    output_ptr.close()
    
if __name__ == '__main__':
    main()
