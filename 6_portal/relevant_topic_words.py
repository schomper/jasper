#! /usr/bin/python3
import sys
import json

count = 0


def process_folder(folder, num_words, parent):
    global count
    vocab = []
    topics = []

    # --- Add vocab to memory --- #
    vocab_ptr = open(folder + '/initial.vocab', 'r')
    line = vocab_ptr.readline()

    while line != '':
        vocab.append(line.strip())
        line = vocab_ptr.readline()

    vocab_ptr.close()

    # for each line in the beta file
    indices = list(range(len(vocab)))

    out = open(folder + '/out/topic_nums.txt', 'w')
    for topic in open(folder + '/out/final.beta', 'r'):
        topic_hash = {}
        topic_words = []

        topic = list(map(float, topic.split()))
        indices = sorted(indices, key=lambda x: -topic[x])

        for i in range(num_words):
            topic_words.append(vocab[indices[i]])

        topic_hash['index'] = count
        topic_hash['label'] = count
        topic_hash['words'] = topic_words
        topic_hash['parent'] = parent

        out.write(str(count) + '\n')
        topics.append(topic_hash)
        count += 1

    return topics


def main():
    if len(sys.argv) != 5:
        print('./relevant_topic_words.py <folder> ' +
              '<number_of_words_per_topic> <num_subs> <output_file>')
        exit(1)

    input_folder = sys.argv[1]
    num_words = int(sys.argv[2])
    num_subs = int(sys.argv[3])
    output_file = sys.argv[4]

    topic_db_object = []

    # Process highest level
    folder = input_folder
    parent = -1
    topic_db_object.extend(process_folder(folder, num_words, parent))

    for i in range(0, num_subs):
        parent = i
        folder = input_folder + '/' + str(i)
        topic_db_object.extend(process_folder(folder, num_words, parent))

    # --- Write to file --- #
    output_ptr = open(output_file, 'w')
    output_ptr.write(json.dumps(topic_db_object, sort_keys=True, indent=4))
    output_ptr.close()


if __name__ == '__main__':
    main()
