import unittest
from ruwiktionary import *


class TestColIndexToPlurality(unittest.TestCase):
    def testNumOneIsSingular(self):
        self.assertEqual('singular', col_idx_to_en_number(1))

    def testNumTwoIsPlural(self):
        self.assertEqual('plural', col_idx_to_en_number(2))

    def testNumZeroIsNone(self):
        self.assertIsNone(col_idx_to_en_number(0))

    def testNumThreeIsNone(self):
        self.assertIsNone(col_idx_to_en_number(3))


class TestWiktionaryURL(unittest.TestCase):
    def testQuotedURL(self):
        expected = 'https://ru.wiktionary.org/wiki/%D1%85%D0%BE%D1%80%D0%BE%D1%88%D0%BE'
        w = RuWikitionary('хорошо', False)
        actual = w.url
        self.assertEqual(expected, actual)
