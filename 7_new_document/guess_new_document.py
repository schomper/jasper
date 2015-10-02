#! /usr/bin/python3
import sys
import json
import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

def main():
    # TODO fill in checking
    document_file = sys.argv[1]
    vocab_file = sys.argv[2]
    vocab_details_file = sys.argv[3]
    output_file = sys.argv[4]

    document_hash = {}

    with open(vocab_file) as data_file:
        vocab_index_data = json.load(data_file)

    with open(vocab_details_file) as data_file:
        vocab_details_data = json.load(data_file)

    document_ptr = open(document_file, 'r')

    line = document_ptr.readline()

    while line != '':
        line = line.strip()
        line = clean_line(line)

        words = line.split(' ')

        for word in words:
            if word == '':
                continue

            # TODO there is a bug here
            if not word in vocab_index_data:
                print('Word is unknown: %s' % word)

            else:
                word_index = str(vocab_index_data[word])
                word_total = vocab_details_data[word_index]['total']
                word_topics = vocab_details_data[word_index]['topics']

                for word_topic in word_topics:

                    if not word_topic in document_hash:
                        print('Adding topic %s' % word_topic)
                        document_hash[word_topic] = 0

                    document_hash[word_topic] += vocab_details_data[word_index]['topics'][word_topic] / word_total

        line = document_ptr.readline()

    document_ptr.close()

    output_ptr = open(output_file, 'w')
    output_ptr.write(json.dumps(document_hash, sort_keys=True, indent=4))
    output_ptr.close()



def clean_line(line):
    stemmer = SnowballStemmer('english')

    # remove digits
    clean_line = ''.join([index for index in line if not index.isdigit()])

    # make words lowercase
    clean_line = clean_line.lower()


    words_list = clean_line.split(' ')

    for word in words_list:
        index = words_list.index(word)

        words_list[index] = word.strip(' ')

        # remove stop words
        if words_list[index] in stopwords.words('english'):
            removed = words_list.pop(index)
            print('removed: %s' % removed)
            continue

        words_list[index] = re.sub(r'\s+', "", word)
        if words_list[index] == '':
            removed = words_list.pop(index)
            print('removed: %s' % removed)
            continue

        words_list[index] = stemmer.stem(word)

    clean_line = ' '.join(words_list)

    print(clean_line)

    return clean_line

if __name__ == "__main__":
    main()
