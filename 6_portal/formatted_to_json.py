#! /usr/bin/python3
import sys
import json


def main():
    overall_dict = {}

    if len(sys.argv) != 2:
        print('./formatted_to_json <formatted_file>')
        exit(1)

    file_name = sys.argv[1]
    file_ptr = open(file_name, 'r')

    line = file_ptr.readline()

    count = 0
    articles = {}

    # Process lines
    while line != '':
        article = {}
        line = line.strip()

        topic_words, date, title, document = line.split('|~|')

        article['Date'] = date
        article['TopicWords'] = topic_words
        article['Title'] = title

        articles[count] = article

        line = file_ptr.readline()
        count += 1

    overall_dict['NumTopics'] = count
    overall_dict['Topics'] = articles

    # write json out
    output_ptr = open('articles.json', 'w')
    output_ptr.write(json.dumps(overall_dict, sort_keys=True, indent=4))
    output_ptr.close()

if __name__ == '__main__':
    main()
