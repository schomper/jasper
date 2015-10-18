#! /usr/bin/python3
import sys
import os
import json

HIERARCHY = False


def isHierarchy(folder):
    """ (string) -> boolean

    Determines if the folder name provided contains a topic hierarchy
    """
    folder_list = os.listdir(folder)

    return '0' in folder_list


def processSingleGammaFile(gamma_file_name):
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


def processSingle(folder):
    count = 0
    articles = []

    gamma_file_name = folder + '/out/final.gamma'
    format_file_name = folder + '/initial.formatted'

    documents_top_topics = processSingleGammaFile(gamma_file_name)

    format_file_ptr = open(format_file_name, 'r')
    line = format_file_ptr.readline()

    # Process lines
    while line != '':
        article = {}
        line = line.strip()

        topic_words, date, title, document = line.split('|~|')

        article['doc_id'] = count
        article['date'] = date
        article['top_topics'] = documents_top_topics[count]
        article['title'] = title

        articles.append(article)

        line = format_file_ptr.readline()
        count += 1

    return articles


def getTopics(line, zero):
    line = line.strip()
    vals = line.split(' ')
    real_vals = []

    for index in range(len(vals)):
        if float(vals[index]) > zero + 0.01:
            real_vals.append(str(index) + ':' + str(vals[index]))

    return real_vals


def getGammaBase(gamma_lines):
    """ (list) -> float

    Return the value assigned to 'nearly impossible' topic
    matching within this gamma file
    """
    zero = 0
    lowest_five = []

    for i in range(5):
        line = gamma_lines[i].strip()
        vals = line.split(' ')

        numbers = [float(val) for val in vals]
        sorted_nums = sorted(numbers)
        lowest_five.append(sorted_nums[0])

    zero = sum(lowest_five) / float(len(lowest_five))

    return zero


def order_topics(topics_hash, topic_ids):
    ordered_topics = []

    for folder in topics_hash:
        for item in topics_hash[folder]:
            sub, prob = item.split(':')
            ordered_topics.append([folder, sub, prob])

    ordered_topics.sort(key=lambda x: float(x[2]), reverse=True)

    ordered_index_topics = []

    for items in ordered_topics:
        ordered_index_topics.append(topic_ids[items[0]][int(items[1])])

    return ordered_index_topics


def processHierarchy(folder):
    articles = []

    files_list = os.listdir(folder)

    document_hash = {}
    topic_ids = {}

    for item in files_list:
        if not item.isdigit():
            continue

        # Read format file
        topic_file = folder + '/' + item + '/out/topic_nums.txt'
        topic_ptr = open(topic_file, 'r')
        topic_lines = topic_ptr.readlines()
        topic_ptr.close()

        topic_indexes = []
        for line in topic_lines:
            topic_indexes.append(line.strip())

        topic_ids[item] = topic_indexes

        # Read format file
        format_file = folder + '/' + item + '/initial.formatted'
        format_ptr = open(format_file, 'r')
        format_lines = format_ptr.readlines()
        format_ptr.close()

        # Read gamma file
        gamma_file = folder + '/' + item + '/out/final.gamma'
        gamma_ptr = open(gamma_file, 'r')
        gamma_lines = gamma_ptr.readlines()
        gamma_ptr.close()

        zero = getGammaBase(gamma_lines)

        # For each document line
        for index in range(len(format_lines)):
            article = {}
            line = format_lines[index].strip()
            doc_id, prob, topic, date, title, data = line.split('|~|')

            article['doc_id'] = doc_id
            article['date'] = date
            article['title'] = title

            if doc_id not in document_hash:
                document_hash[doc_id] = {}
                document_hash[doc_id]['topics'] = {}

            document_hash[doc_id]['topics'][item] = \
                getTopics(gamma_lines[index], zero)
            document_hash[doc_id]['article'] = article

    for doc in document_hash:
        document_hash[doc]['article']['topics'] = \
            order_topics(document_hash[doc]['topics'], topic_ids)

        articles.append(document_hash[doc]['article'])

    return articles


def main():
    global HIERARCHY

    if len(sys.argv) != 3:
        print('./document_list_generator <folder> <output_file>')
        exit(1)

    folder_name = sys.argv[1]
    output_file_name = sys.argv[2]

    HIERARCHY = isHierarchy(folder_name)

    if HIERARCHY:
        articles = processHierarchy(folder_name)
    else:
        articles = processSingle(folder_name)

    # write json out
    output_ptr = open(output_file_name, 'w')
    output_ptr.write(json.dumps(articles, sort_keys=True, indent=4))
    output_ptr.close()

if __name__ == '__main__':
    main()
