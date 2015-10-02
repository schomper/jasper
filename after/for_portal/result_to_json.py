#! /usr/bin/python3
import sys
import json

def main():
    
    overall_array = []
    overall_dict = {}

    if len(sys.argv) != 2:
        print('./result_to_json <result_file>');    
        exit(1)

    file_name = sys.argv[1]
    
    file_ptr = open(file_name, 'r')

    line = file_ptr.readline()

    count = 0
    
    topics = {}
    topic_words = []

    # Process lines
    while line != '':
        line = line.strip()
        
        if 'Topic' in line:
            if count != 0:
                topics[version] = topic_words
            topic, version = line.split(' ');
            
            topic_words = []
            count += 1

      
        elif line == '':
            line = file_ptr.readline()
            continue
        
        else:
            topic_words.append(line)
            

        line = file_ptr.readline()
        
    topics[version] = topic_words
    
    overall_dict['NumTopics'] = count
    overall_dict['Topics'] = topics

    # write json out
    output_ptr = open('result.json', 'w')
    output_ptr.write(json.dumps(overall_dict, sort_keys=True, indent=4))
    output_ptr.close()
    
if __name__ == '__main__':
    main()
