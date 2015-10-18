#! /usr/bin/python3

# ------------------------------------------------------------------------------
# Name: gen_vocab_file.py
#
# Usage: script takes a directory containing all the documents as input and
# produces rewrites them in a formatted file. It also produces a vocab file
# ------------------------------------------------------------------------------
import sys
from pathlib import Path
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

vocab = {}
word_index = 0


def strip_line(line, ltoken, rtoken):
    if line.startswith(ltoken):
        line = line[len(ltoken):]
    if line.endswith(rtoken):
        line = line[:-len(rtoken)]
    return line


def remove_digits(line):
    """ (str) -> str

    Return passed in string without any digits in it
    """
    digitless = []
    tokens = list(line)

    for token in tokens:
        if not token.isdigit():
            digitless.append(token)

    line = ''.join(digitless)

    digitless = []
    tokens = line.split(' ')
    for token in tokens:
        if token != '':
            digitless.append(token)

    return ' '.join(digitless)


def stem_line(line):
    """ (str) -> str

    Return passed in string with all words stemmed
    """
    stemmer = SnowballStemmer('english')

    tokens = line.split(' ')
    tokens = [stemmer.stem(token) for token in tokens]

    return ' '.join(tokens)


def remove_stop_words(line):
    """ (str) -> str

    Return passed in string with all stop words removed
    """
    stopless = []
    tokens = line.split(' ')

    for token in tokens:
        if token not in stopwords.words('english'):
            stopless.append(token)

    return ' '.join(stopless)


def clean_line(line):
    """ (str) -> str

    Return the string after stemming the words
    """
    line = line.lower()
    line = remove_digits(line)
    line = remove_stop_words(line)
    line = stem_line(line)

    return line


def get_date(line):
    assert('<Date>' in line)
    return strip_line(line, '<Date>', '</Date>\n')


def get_title(line):
    assert('<Title>' in line)
    return strip_line(line, '<Title>', '</Title>\n')


def get_topic(line):
    assert('<Topic>' in line)
    return strip_line(line, '<Topic>', '</Topic>\n')


def format_line(line):
    global vocab
    words = {}

    tokens = line.split(' ')

    for token in tokens:
        if token not in words:
            words[token] = 1
        else:
            words[token] += 1

        if token not in vocab:
            vocab[token] = 0

        vocab[token] += 1

    info = str(len(words))
    for key in words:
        info += ' ' + key + ':' + str(words[key])

    return info


def get_contents(line):
    assert('<Contents>' in line)

    line = strip_line(line, '<Contents>', '</Contents>\n')
    line = clean_line(line)
    line = format_line(line)

    return line


def process_corpus(lines):
    """ (list) -> list

    Takes a list of all lines in the corpus, returns a list of documents
    """
    count = 0
    documents = []

    while len(lines) != 0:
        if count % 1000 == 0:
            print('\t processing document ' + str(count))

        document = []
        topic = get_topic(lines.pop(0))
        date = get_date(lines.pop(0))
        title = get_title(lines.pop(0))
        contents = get_contents(lines.pop(0))

        document.append(topic)
        document.append(date)
        document.append(title)
        document.append(contents)

        documents.append(document)
        count += 1

    return documents


def correct_vocab(vocab, threshold):

    remove_keys = []
    for key in vocab:
        if int(vocab[key]) <= threshold:
            remove_keys.append(key)

    for key in remove_keys:
        vocab.pop(key, None)

    good_vocab = []
    for key in vocab:
        good_vocab.append(key)

    return good_vocab


def get_fixed_contents(contents, good_vocab):

    items = contents.split(' ')
    correct_items = []
    items.pop(0)
    for item in items:
        word, count = item.split(':')
        if word not in good_vocab:
            continue

        index = good_vocab.index(word)
        correct_items.append(str(index) + ':' + str(count))

    num_words = len(correct_items)

    if num_words == 0:
        return None

    info_line = ''
    info_line += str(num_words)

    for item in correct_items:
        info_line += ' ' + item

    return info_line


def correct_documents(good_vocab, documents):

    correct = []
    count = 0
    for document in documents:
        if count % 1000 == 0:
            print('\tprocessing document ' + str(count))

        document[3] = get_fixed_contents(document[3], good_vocab)

        if document[3] != None:
            correct.append(document)

        count += 1

    return correct


def print_corpus(documents, vocab, output):
    output_file = open(output + '\initial.formatted', 'w')

    for document in documents:
        output_file.write('|~|'.join(document) + '\n')

    output_file.close()

    output_file = open(output + '\c_lda.formatted', 'w')

    for document in documents:
        output_file.write(document[3] + '\n')

    output_file.close()

    vocab_file = open(output + '\initial.vocab', 'w')

    for word in vocab:
        vocab_file.write("%s\n" % word)

    vocab_file.close()


def main():
    """ Main function for program """
    global vocab

    if len(sys.argv) != 5:
        print('usage: gen_vocab_file.py <input_directory> ' +
              '<threshold> <output_directory> <folder/file>')
        sys.exit(1)

    input_directory = Path(sys.argv[1])
    threshold = int(sys.argv[2])
    output_directory = sys.argv[3]
    setting = sys.argv[4]

    corpus_lines = []
    print('Getting corpus files')
    if setting == 'folder':
        for year_directory in input_directory.iterdir():
            for day_file in year_directory.iterdir():
                with day_file.open() as f:
                    day_lines = f.readlines()

                corpus_lines = corpus_lines + day_lines

    else:
        with input_directory.open() as f:
            day_lines = f.readlines()

        corpus_lines = corpus_lines + day_lines

    print('Processing corpus')
    documents = process_corpus(corpus_lines)

    print(str(vocab))
    print('Getting good vocab')
    good_vocab = correct_vocab(vocab, threshold)

    print('Correcting documents')
    documents = correct_documents(good_vocab, documents)

    print(str(documents))
    print_corpus(documents, good_vocab, output_directory)


if __name__ == '__main__':
    vocab = {}

    main()
