import unittest
from grammar import *
from ruwiktionary import *


class TestPossessivePronoun(unittest.TestCase):
    def testPossessivePronounCodePrefix(self):
        self.assertEqual('pronoun_possessive', PossessivePronoun('test').code_prefix())


class TestCanParsePossessivePronounA(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = RuWikitionary('свой', True, 'poss_pronoun_свой.html')
        cls.pronoun: PossessivePronoun = cls.page.parse_possessive_pronoun()

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
        self.assertEqual(self.page.pos, SpeechPart.PRONOUN_POSSESSIVE)

    def testCanParseNominativeMasculine(self):
        """
        Test that we can extract the nominative masculine form
        :return:
        """
        actual = self.pronoun.nominative.masculine
        self.assertIn('свой', actual)

    def testCanParseNominativeFeminine(self):
        """
        Test that we can extract the nominative feminine form
        :return: Nothing
        """
        actual = self.pronoun.nominative.feminine
        self.assertIn('своя́', actual)

    def testCanParseNominativeNeuter(self):
        """
        Test that we can extract the nominative neuter form
        :return: Nothing
        """
        actual = self.pronoun.nominative.neuter
        self.assertIn('своё', actual)

    def testCanParseNominativePlural(self):
        """
        Test that we can extract the nominative plural form
        :return: Nothing
        """
        actual = self.pronoun.nominative.plural
        self.assertIn('свои́', actual)

    def testCanParseGenitiveMasculine(self):
        """
        Test that we can extract the genitive masculine form
        :return:
        """
        actual = self.pronoun.genitive.masculine
        self.assertIn('своего́', actual)

    def testCanParseGenitiveFeminine(self):
        """
        Test that we can extract the genitive feminine form
        :return: Nothing
        """
        actual = self.pronoun.genitive.feminine
        self.assertIn('свое́й', actual)

    def testCanParseGenitiveNeuter(self):
        """
        Test that we can extract the genitive neuter form
        :return: Nothing
        """
        actual = self.pronoun.genitive.neuter
        self.assertIn('своего́', actual)

    def testCanParseGenitivePlural(self):
        """
        Test that we can extract the genitive plural form
        :return: Nothing
        """
        actual = self.pronoun.genitive.plural
        self.assertIn('свои́х', actual)

    def testCanParseDativeMasculine(self):
        """
        Test that we can extract the dative masculine form
        :return:
        """
        actual = self.pronoun.dative.masculine
        self.assertIn('своему́', actual)

    def testCanParseDativeFeminine(self):
        """
        Test that we can extract the dative feminine form
        :return: Nothing
        """
        actual = self.pronoun.dative.feminine
        self.assertIn('свое́й', actual)

    def testCanParseDativeNeuter(self):
        """
        Test that we can extract the dative neuter form
        :return: Nothing
        """
        actual = self.pronoun.dative.neuter
        self.assertIn('своему́', actual)

    def testCanParseDativePlural(self):
        """
        Test that we can extract the dative plural form
        :return: Nothing
        """
        actual = self.pronoun.dative.plural
        self.assertIn('свои́м', actual)

    def testCanParseAccusativeInanimateMasculine(self):
        """
        Test that we can extract the accusative inanimate masculine form
        :return:
        """
        actual = self.pronoun.accusative_inanimate.masculine
        self.assertIn('свой', actual)

    def testCanParseAccusativeInanimateFeminine(self):
        """
        Test that we can extract the accusative inanimate feminine form
        :return: Nothing
        """
        actual = self.pronoun.accusative_inanimate.feminine
        self.assertIn('свою́', actual)

    def testCanParseAccusativeInanimateNeuter(self):
        """
        Test that we can extract the accusative inanimate neuter form
        :return: Nothing
        """
        actual = self.pronoun.accusative_inanimate.neuter
        self.assertIn('своё', actual)

    def testCanParseAccusativeInanimatePlural(self):
        """
        Test that we can extract the accusative inanimate plural form
        :return: Nothing
        """
        actual = self.pronoun.accusative_inanimate.plural
        self.assertIn('свои́', actual)

    def testCanParseAccusativeAnimateMasculine(self):
        """
        Test that we can extract the accusative animate masculine form
        :return:
        """
        actual = self.pronoun.accusative_animate.masculine
        self.assertIn('своего́', actual)

    def testCanParseAccusativeAnimateFeminine(self):
        """
        Test that we can extract the accusative animate feminine form
        :return: Nothing
        """
        actual = self.pronoun.accusative_animate.feminine
        self.assertIn('свою́', actual)

    def testCanParseAccusativeAnimateNeuter(self):
        """
        Test that we can extract the accusative animate neuter form
        :return: Nothing
        """
        actual = self.pronoun.accusative_animate.neuter
        self.assertIn('своё', actual)

    def testCanParseAccusativeAnimatePlural(self):
        """
        Test that we can extract the accusative animate plural form
        :return: Nothing
        """
        actual = self.pronoun.accusative_animate.plural
        self.assertIn('свои́х', actual)

    def testCanParseInstrumentalMasculine(self):
        actual = self.pronoun.instrumental.masculine
        self.assertIn('свои́м', actual)

    def testCanParseInstrumentalFeminine(self):
        actual = self.pronoun.instrumental.feminine
        self.assertIn('свое́й', actual)
        self.assertIn('свое́ю', actual)

    def testCanParseInstrumentalNeuter(self):
        actual = self.pronoun.instrumental.neuter
        self.assertIn('свои́м', actual)

    def testCanParseInstrumentalPlural(self):
        actual = self.pronoun.instrumental.plural
        self.assertIn('свои́ми', actual)

    def testCanParsePrepositionalMasculine(self):
        self.assertIn('своём', self.pronoun.prepositional.masculine)

    def testCanParsePrepositionalNeuter(self):
        self.assertIn('своём', self.pronoun.prepositional.neuter)

    def testCanParsePrepositionalFeminine(self):
        self.assertIn('свое́й', self.pronoun.prepositional.feminine)

    def testCanParsePrepositionalPlural(self):
        self.assertIn('свои́х', self.pronoun.prepositional.plural)