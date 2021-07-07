import unittest
from grammar import *
from ruwiktionary import *


class TestParsePrepositionA(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = RuWikitionary('к', True, 'preposition_к.html')

    def testThatPageIsSet(self):
        """
        Test that we can load page
        :return: Nothing
        """
        self.assertIsNotNone(self.page)

    def testCanParsePage(self):
        """
        Test that we can generate a page tree
        :return: Nothing
        """
        self.assertIsNotNone(self.page.root_tree)

    def testCanExtractSpeechPart(self):
        self.assertEqual(self.page.pos, SpeechPart.PREPOSITION)