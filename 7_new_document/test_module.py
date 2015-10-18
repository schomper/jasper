#! /usr/bin/python3
import unittest
from utils import *


class TestUtils(unittest.TestCase):

    # TODO: def test_remove_stopwords(self):

    # TODO: def test_clean_line(self):

    # TODO: def test_stem_line(self):

    # TODO: def test_check_start(self):

    def test_remove_digits(self):
        test_string1 = '2'
        test_string2 = 'l10n'
        test_string3 = 'lion 9'
        test_string4 = 'lion 7 was there'
        test_string5 = 'lion 71 was there'
        test_string6 = 'lion 71 was 1 there'

        expect_string1 = ''
        expect_string2 = 'ln'
        expect_string3 = 'lion'
        expect_string4 = 'lion was there'
        expect_string5 = 'lion was there'
        expect_string6 = 'lion was there'

        self.assertEqual(remove_digits(test_string1), expect_string1)
        self.assertEqual(remove_digits(test_string2), expect_string2)
        self.assertEqual(remove_digits(test_string3), expect_string3)
        self.assertEqual(remove_digits(test_string4), expect_string4)
        self.assertEqual(remove_digits(test_string5), expect_string5)
        self.assertEqual(remove_digits(test_string6), expect_string6)

# TODO: class TestGenerateTopicsList(unittest.TestCase):


# TODO: class TestGuessNewDocument(unittest.TestCase):


# TODO: class TestFindVocabTopics(unittest.TestCase):


# TODO: class TestFindIndexWord(unittest.TestCase):


# TODO: class TestAnalyseDocumentClassification(unittest.TestCase):


if __name__ == '__main__':
    unittest.main()
