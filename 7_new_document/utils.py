import sys
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


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


def check_start(message, amount):
    """ (str, int) ->

    Abort the start if sys.argv not equal to required amount
    """
    if len(sys.argv) != amount:
        print(message)
        exit(1)
