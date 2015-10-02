#! /usr/bin/python3
import sys
import json

def process_gamma_file(gamma_file_name):
    documents_top_topics = []

    gamma_file_ptr = open(gamma_file_name, 'r')

    line = gamma_file_ptr.readline()

    while line != '':
        topics = [float(x) for x in line.split()]
        indices = list(range(len(topics)))
        indices = sorted(indices, key=lambda x: -topics[x])

        documents_top_topics.append(indices)

        line = line.strip()
        line = gamma_file_ptr.readline()

    gamma_file_ptr.close()

    return documents_top_topics

def main():

    overall_dict = {}

    if len(sys.argv) != 4:
        print('./document_list_generator <formatted_file> <gamma_file> <output_file>');
        exit(1)

    format_file_name = sys.argv[1]
    gamma_file_name = sys.argv[2]
    output_file_name = sys.argv[3]

    documents_top_topics = process_gamma_file(gamma_file_name)

    format_file_ptr = open(format_file_name, 'r')

    line = format_file_ptr.readline()

    count = 0

    articles = {}

    # Process lines
    while line != '':
        article = {}
        line = line.strip()

        topic_words, date, title, document = line.split('|~|')

        article['date'] = date
        try:
            article['top_topics'] = documents_top_topics[count]
        except:
            print(count)

        article['title'] = title

        articles[count] = article

        line = format_file_ptr.readline()
        count += 1

    overall_dict['num_articles'] = count
    overall_dict['articles'] = articles

    # write json out
    output_ptr = open(output_file_name, 'w')
    output_ptr.write(json.dumps(overall_dict, sort_keys=True, indent=4))
    output_ptr.close()

if __name__ == '__main__':
    main()
