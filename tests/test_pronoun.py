import unittest
from grammar import *
from ruwiktionary import *


class TestPronounA(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = RuWikitionary('кто', True, 'pronoun_кто.html')
        cls.pronoun: Pronoun = cls.page.parse_pronoun()

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
        self.assertEqual(self.page.pos, SpeechPart.PRONOUN)

    def testCanParseNominative(self):
        self.assertEqual('кто́', self.pronoun.nominative)

    def testCanParseGenitive(self):
        self.assertEqual('кого́', self.pronoun.genitive)

    def testCanParseDative(self):
        self.assertEqual('кому́', self.pronoun.dative)

    def testCanParseAccusative(self):
        self.assertEqual('кого́', self.pronoun.accusative)

    def testCanParseInstrumental(self):
        self.assertEqual('ке́м', self.pronoun.instrumental)

    def testCanParsePrepositional(self):
        self.assertEqual('ком', self.pronoun.prepositional)


class TestPronounB(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = RuWikitionary('что', True, 'pronoun_что.html')
        cls.pronoun: Pronoun = cls.page.parse_pronoun()

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
        self.assertEqual(self.page.pos, SpeechPart.PRONOUN)

    def testCanParseNominative(self):
        self.assertEqual('что́', self.pronoun.nominative)

    def testCanParseGenitive(self):
        self.assertEqual('чего́', self.pronoun.genitive)

    def testCanParseDative(self):
        self.assertEqual('чему́', self.pronoun.dative)

    def testCanParseAccusative(self):
        self.assertEqual('что́', self.pronoun.accusative)

    def testCanParseInstrumental(self):
        self.assertEqual('чем', self.pronoun.instrumental)

    def testCanParsePrepositional(self):
        self.assertEqual('чём', self.pronoun.prepositional)