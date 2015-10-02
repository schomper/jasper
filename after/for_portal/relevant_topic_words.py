#! /usr/bin/python3
import sys
import json

def main():

    if len(sys.argv) != 5:
        # TODO make this meaningful
        print('./relevant_topic_words.py <beta_file> <vocab_file> <number_of_words_per_topic> <output_file>')
        exit(1)

    input_file = sys.argv[1]
    vocab_file = sys.argv[2]
    num_words = int(sys.argv[3])
    output_file = sys.argv[4]

    #--- Add vocab to memory ---#
    vocab = []
    vocab_ptr = open(vocab_file, 'r')
    line = vocab_ptr.readline()

    while line != '':
        vocab.append(line.strip())
        line = vocab_ptr.readline()

    vocab_ptr.close()

    topics = []
    # for each line in the beta file
    indices = list(range(len(vocab)))

    for topic in open(input_file, 'r'):
        topic_words = []

        topic = list(map(float, topic.split()))
        indices = sorted(indices, key=lambda x: -topic[x])

        for i in range(num_words):
            topic_words.append(vocab[indices[i]])

        topics.append(topic_words)


    #--- Write to file ---#
    output_ptr = open(output_file, 'w')
    output_ptr.write(json.dumps(topics, sort_keys=True, indent=4)) #TODO
    output_ptr.close()


if __name__ == '__main__':
    main()
