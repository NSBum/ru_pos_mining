import unittest
from grammar import *
from ruwiktionary import *


class TestCanParseDemonstrativePronounA(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = RuWikitionary('этот', True, 'demonstrative_pronoun_этот.html')
        cls.pronoun: DemonstrativePronoun = cls.page.parse_demonstrative_pronoun()

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
        self.assertEqual(self.page.pos, SpeechPart.PRONOUN_DEMONSTRATIVE)

    def testCanParseNominativeMasculine(self):
        self.assertIn(self.pronoun.nominative.masculine, 'э́тот')

    def testCanParseNominativeFeminine(self):
        self.assertIn(self.pronoun.nominative.feminine, 'э́та')

    def testCanParseNominativeNeuter(self):
        self.assertIn(self.pronoun.nominative.neuter, 'э́то')

    def testCanParseNominativePlural(self):
        self.assertIn(self.pronoun.nominative.plural, 'э́ти')

    def testCanParseGenitiveMasculine(self):
        self.assertIn(self.pronoun.genitive.masculine, 'э́того')

    def testCanParseGenitiveFeminine(self):
        self.assertIn(self.pronoun.genitive.feminine, 'э́той')

    def testCanParseGenitiveNeuter(self):
        self.assertIn(self.pronoun.genitive.neuter, 'э́того')

    def testCanParseGenitivePlural(self):
        self.assertIn(self.pronoun.genitive.plural, 'э́тих')