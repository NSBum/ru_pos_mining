import unittest
from grammar import *
from ruwiktionary import *


class TestAdjective(unittest.TestCase):
    def testAdjectiveCodePrefix(self):
        self.assertEqual('adj', Adjective('test').code_prefix())


class TestCanParseAdjectiveA(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = RuWikitionary('хороший', True, 'adj_sample_01.html')
        cls.adjective: Adjective = cls.page.parse_adjective()

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

    def testCanParseNominativeMasculine(self):
        """
        Test that we can extract the nominative masculine form
        :return:
        """
        actual = self.adjective.nominative.masculine
        self.assertIn('хоро́ший', actual)

    def testCanParseNominativeFeminine(self):
        """
        Test that we can extract the nominative feminine form
        :return: Nothing
        """
        actual = self.adjective.nominative.feminine
        self.assertIn('хоро́шая', actual)

    def testCanParseNominativeNeuter(self):
        """
        Test that we can extract the nominative neuter form
        :return: Nothing
        """
        actual = self.adjective.nominative.neuter
        self.assertIn('хоро́шее', actual)

    def testCanParseNominativePlural(self):
        """
        Test that we can extract the nominative plural form
        :return: Nothing
        """
        actual = self.adjective.nominative.plural
        self.assertIn('хоро́шие', actual)

    def testCanParseGenitiveMasculine(self):
        """
        Test that we can extract the genitive masculine form
        :return:
        """
        actual = self.adjective.genitive.masculine
        self.assertIn('хоро́шего', actual)

    def testCanParseGenitiveFeminine(self):
        """
        Test that we can extract the genitive feminine form
        :return: Nothing
        """
        actual = self.adjective.genitive.feminine
        self.assertIn('хоро́шей', actual)

    def testCanParseGenitiveNeuter(self):
        """
        Test that we can extract the genitive neuter form
        :return: Nothing
        """
        actual = self.adjective.genitive.neuter
        self.assertIn('хоро́шего', actual)

    def testCanParseGenitivePlural(self):
        """
        Test that we can extract the genitive plural form
        :return: Nothing
        """
        actual = self.adjective.genitive.plural
        self.assertIn('хоро́ших', actual)

    def testCanParseDativeMasculine(self):
        """
        Test that we can extract the dative masculine form
        :return:
        """
        actual = self.adjective.dative.masculine
        self.assertIn('хоро́шему', actual)

    def testCanParseDativeFeminine(self):
        """
        Test that we can extract the dative feminine form
        :return: Nothing
        """
        actual = self.adjective.dative.feminine
        self.assertIn('хоро́шей', actual)

    def testCanParseDativeNeuter(self):
        """
        Test that we can extract the dative neuter form
        :return: Nothing
        """
        actual = self.adjective.dative.neuter
        self.assertIn('хоро́шему', actual)

    def testCanParseDativePlural(self):
        """
        Test that we can extract the dative plural form
        :return: Nothing
        """
        actual = self.adjective.dative.plural
        self.assertIn('хоро́шим', actual)

    def testCanParseAccusativeInanimateMasculine(self):
        """
        Test that we can extract the accusative inanimate masculine form
        :return:
        """
        actual = self.adjective.accusative_inanimate.masculine
        self.assertIn('хоро́ший', actual)

    def testCanParseAccusativeInanimateFeminine(self):
        """
        Test that we can extract the accusative inanimate feminine form
        :return: Nothing
        """
        actual = self.adjective.accusative_inanimate.feminine
        self.assertIn('хоро́шую', actual)

    def testCanParseAccusativeInanimateNeuter(self):
        """
        Test that we can extract the accusative inanimate neuter form
        :return: Nothing
        """
        actual = self.adjective.accusative_inanimate.neuter
        self.assertIn('хоро́шее', actual)

    def testCanParseAccusativeInanimatePlural(self):
        """
        Test that we can extract the accusative inanimate plural form
        :return: Nothing
        """
        actual = self.adjective.accusative_inanimate.plural
        self.assertIn('хоро́шие', actual)

    def testCanParseAccusativeAnimateMasculine(self):
        """
        Test that we can extract the accusative animate masculine form
        :return:
        """
        actual = self.adjective.accusative_animate.masculine
        self.assertIn('хоро́шего', actual)

    def testCanParseAccusativeAnimateFeminine(self):
        """
        Test that we can extract the accusative animate feminine form
        :return: Nothing
        """
        actual = self.adjective.accusative_animate.feminine
        self.assertIn('хоро́шую', actual)

    def testCanParseAccusativeAnimateNeuter(self):
        """
        Test that we can extract the accusative animate neuter form
        :return: Nothing
        """
        actual = self.adjective.accusative_animate.neuter
        self.assertIn('хоро́шее', actual)

    def testCanParseAccusativeAnimatePlural(self):
        """
        Test that we can extract the accusative animate plural form
        :return: Nothing
        """
        actual = self.adjective.accusative_animate.plural
        self.assertIn('хоро́ших', actual)

# дурацкий


class TestCanParseAdjectiveB(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = RuWikitionary('дурацкий', True, 'adj_sample_02.html')
        cls.adjective: Adjective = cls.page.parse_adjective()

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

    def testCanParseNominativeMasculine(self):
        """
        Test that we can extract the nominative masculine form
        :return:
        """
        actual = self.adjective.nominative.masculine
        self.assertIn('дура́цкий', actual)

    def testCanParseNominativeFeminine(self):
        """
        Test that we can extract the nominative feminine form
        :return: Nothing
        """
        actual = self.adjective.nominative.feminine
        self.assertIn('дура́цкая', actual)

    def testCanParseNominativeNeuter(self):
        """
        Test that we can extract the nominative neuter form
        :return: Nothing
        """
        actual = self.adjective.nominative.neuter
        self.assertIn('дура́цкое', actual)

    def testCanParseNominativePlural(self):
        """
        Test that we can extract the nominative plural form
        :return: Nothing
        """
        actual = self.adjective.nominative.plural
        self.assertIn('дура́цкие', actual)

    def testCanParseGenitiveMasculine(self):
        """
        Test that we can extract the genitive masculine form
        :return:
        """
        actual = self.adjective.genitive.masculine
        self.assertIn('дура́цкого', actual)

    def testCanParseGenitiveFeminine(self):
        """
        Test that we can extract the genitive feminine form
        :return: Nothing
        """
        actual = self.adjective.genitive.feminine
        self.assertIn('дура́цкой', actual)

    def testCanParseGenitiveNeuter(self):
        """
        Test that we can extract the genitive neuter form
        :return: Nothing
        """
        actual = self.adjective.genitive.neuter
        self.assertIn('дура́цкого', actual)

    def testCanParseGenitivePlural(self):
        """
        Test that we can extract the genitive plural form
        :return: Nothing
        """
        actual = self.adjective.genitive.plural
        self.assertIn('дура́цких', actual)

    def testCanParseDativeMasculine(self):
        """
        Test that we can extract the dative masculine form
        :return:
        """
        actual = self.adjective.dative.masculine
        self.assertIn('дура́цкому', actual)

    def testCanParseDativeFeminine(self):
        """
        Test that we can extract the dative feminine form
        :return: Nothing
        """
        actual = self.adjective.dative.feminine
        self.assertIn('дура́цкой', actual)

    def testCanParseDativeNeuter(self):
        """
        Test that we can extract the dative neuter form
        :return: Nothing
        """
        actual = self.adjective.dative.neuter
        self.assertIn('дура́цкому', actual)

    def testCanParseDativePlural(self):
        """
        Test that we can extract the dative plural form
        :return: Nothing
        """
        actual = self.adjective.dative.plural
        self.assertIn('дура́цким', actual)

    def testCanParseAccusativeInanimateMasculine(self):
        """
        Test that we can extract the accusative inanimate masculine form
        :return:
        """
        actual = self.adjective.accusative_inanimate.masculine
        self.assertIn('дура́цкий', actual)

    def testCanParseAccusativeInanimateFeminine(self):
        """
        Test that we can extract the accusative inanimate feminine form
        :return: Nothing
        """
        actual = self.adjective.accusative_inanimate.feminine
        self.assertIn('дура́цкую', actual)

    def testCanParseAccusativeInanimateNeuter(self):
        """
        Test that we can extract the accusative inanimate neuter form
        :return: Nothing
        """
        actual = self.adjective.accusative_inanimate.neuter
        self.assertIn('дура́цкое', actual)

    def testCanParseAccusativeInanimatePlural(self):
        """
        Test that we can extract the accusative inanimate plural form
        :return: Nothing
        """
        actual = self.adjective.accusative_inanimate.plural
        self.assertIn('дура́цкие', actual)

    def testCanParseAccusativeAnimateMasculine(self):
        """
        Test that we can extract the accusative animate masculine form
        :return:
        """
        actual = self.adjective.accusative_animate.masculine
        self.assertIn('дура́цкого', actual)

    def testCanParseAccusativeAnimateFeminine(self):
        """
        Test that we can extract the accusative animate feminine form
        :return: Nothing
        """
        actual = self.adjective.accusative_animate.feminine
        self.assertIn('дура́цкую', actual)

    def testCanParseAccusativeAnimateNeuter(self):
        """
        Test that we can extract the accusative animate neuter form
        :return: Nothing
        """
        actual = self.adjective.accusative_animate.neuter
        self.assertIn('дура́цкое', actual)

    def testCanParseAccusativeAnimatePlural(self):
        """
        Test that we can extract the accusative animate plural form
        :return: Nothing
        """
        actual = self.adjective.accusative_animate.plural
        self.assertIn('дура́цких', actual)