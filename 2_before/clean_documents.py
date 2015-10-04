#! /usr/bin/python3
import os
import sys
from nltk.corpus import stopwords


def get_documents(year, input_directory, filename):
    global undef_count

    documents_list = []

    read_file = open(input_directory + str(year) + '/' + filename, 'r')
    line = read_file.readline()

    day, month = filename.split('.')[0].split('_')

    while line != '':
        if(line == '<DOC>\n'):
            document = []

            #################################
            # Add date to document
            #################################
            document.append(day + ' ' + month + ' ' + str(year))

            #################################
            # Add title to document
            #################################
            line = read_file.readline()

            # Remove tags
            if line.startswith('<DOC_NAME>'):
                line = line[10:]
            if line.endswith('</DOC_NAME>\n'):
                line = line[:-12]

            document.append(line)

            #################################
            # Add contents to document
            #################################
            topic = ''

            # remove <TEXT> tag
            read_file.readline()

            line = read_file.readline().strip()

            # split into topic and contents
            parts = line.rsplit('Topics', 1)
            line = parts[0]

            if len(parts) == 1:
                topic = 'UNDEFINED'
                undef_count += 1
            else:
                topic = parts[1]

            # remove </TEXT> tag
            read_file.readline()

            line = clean_line(line)
            document.append(line)

            #################################
            # Add topic to document
            #################################

            topic = clean_topics(topic)
            document.append(topic)

            # remove </DOC> tag
            read_file.readline()

            documents_list.append(document)
            line = read_file.readline()

        else:
            print('Should never get here!\n')
            exit(1)

    read_file.close()
    return documents_list


def clean_topics(topic):
    global topics

    # remove first posted date
    clean_topic = topic.rsplit('First posted')[0]

    # remove more stories babble
    clean_topic = clean_topic.rsplit('More stories')[0]

    # remove digits (area codes)
    clean_topic = ''.join(i for i in clean_topic if not i.isdigit())

    clean_topic = clean_topic.strip(' ')

    # pick only the first topic
    clean_topic = clean_topic.split(' ')[0]

    if clean_topic not in topics:
        topics.append(clean_topic)

    return clean_topic


def clean_line(line):
    # remove source information
    source_split = line.rsplit('Source', 1)
    line = source_split[0]

    # remove digits
    clean_line = ''.join([index for index in line if not index.isdigit()])

    # make words lowercase
    clean_line = clean_line.lower()

    # remove stop words
    words_list = clean_line.split(' ')
    for word in words_list:
        if word in stopwords.words('english'):
            words_list.remove(word)

    clean_line = ' '.join(words_list)

    return clean_line


def main():
    global topics
    doc_count = 0

    if len(sys.argv) != 5:
        print('./clean_documents <input_directory> <start_year> <end_year> <output_directory>')
        exit(1)

    input_directory = sys.argv[1]
    start_year = int(sys.argv[2])
    end_year = int(sys.argv[3])
    output_directory = sys.argv[4]

    if not os.path.exists('clean.d/'):
        os.makedirs('clean.d/')

    for year in range(start_year, end_year + 1):
        if not os.path.exists(output_directory + '/clean.d/' + str(year)):
            os.makedirs(output_directory + 'clean.d/' + str(year))

        for filename in os.listdir(input_directory + str(year)):
            document_list = get_documents(year, input_directory, filename)
            doc_count += len(document_list)

            # reformat date in file name correctly
            filedate, filename_suffix = filename.rsplit('.')
            filename_suffix = '.' + filename_suffix

            day, month = filedate.split('_')
            filename = month + '_' + day + filename_suffix

            new_file = open(output_directory + '/clean.d/' + str(year) +
                            '/' + filename, 'w')

            for document in document_list:
                if document[2] != '':
                    new_file.write('<Topic>' + document[3] + '</Topic>\n')
                    new_file.write('<Date>' + document[0] + '</Date>\n')
                    new_file.write('<Title>' + document[1] + '</Title>\n')
                    new_file.write('<Contents>' + document[2] + '</Contents>\n')

            new_file.close()

    print(str(doc_count) + '\n')
    print('Undefined: ' + str(undef_count))

if __name__ == '__main__':
    topics = []
    undef_count = 0
    main()
