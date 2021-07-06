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

    def testCanParseDativeMasculine(self):
        self.assertIn(self.pronoun.dative.masculine, 'э́тому')

    def testCanParseDativeFeminine(self):
        self.assertIn(self.pronoun.dative.feminine, 'э́той')

    def testCanParseDativeNeuter(self):
        self.assertIn(self.pronoun.dative.neuter, 'э́тому')

    def testCanParseDativePlural(self):
        self.assertIn(self.pronoun.dative.plural, 'э́тим')

    def testCanParseAccusativeInanimateMasculine(self):
        self.assertIn(self.pronoun.accusative_inanimate.masculine, 'э́тот')

    def testCanParseAccusativeInanimateFeminine(self):
        self.assertIn(self.pronoun.accusative_inanimate.feminine, 'э́ту')

    def testCanParseAccusativeInanimateNeuter(self):
        self.assertIn(self.pronoun.accusative_inanimate.neuter, 'э́то')

    def testCanParseAccusativeInanimatePlural(self):
        self.assertIn(self.pronoun.accusative_inanimate.plural, 'э́ти')

    def testCanParseAccusativeAnimateMasculine(self):
        self.assertIn(self.pronoun.accusative_animate.masculine, 'э́того')

    def testCanParseAccusativeAnimateFeminine(self):
        self.assertIn(self.pronoun.accusative_animate.feminine, 'э́ту')

    def testCanParseAccusativeAanimateNeuter(self):
        self.assertIn(self.pronoun.accusative_animate.neuter, 'э́то')

    def testCanParseAccusativeAnimatePlural(self):
        self.assertIn(self.pronoun.accusative_animate.plural, 'э́тих')

    def testCanParseInstrumentalMasculine(self):
        self.assertIn(self.pronoun.instrumental.masculine, 'э́тим')

    def testCanParseInstrumentalFeminine(self):
        self.assertIn('э́той', self.pronoun.instrumental.feminine)
        self.assertIn('э́тою', self.pronoun.instrumental.feminine)

    def testCanParseInstrumentalNeuter(self):
        self.assertIn(self.pronoun.instrumental.neuter, 'э́тим')

    def testCanParseInstrumentalPlural(self):
        self.assertIn(self.pronoun.instrumental.plural, 'э́тими')

    def testCanParsePrepositionalMasculine(self):
        self.assertIn('э́том', self.pronoun.prepositional.masculine)

    def testCanParsePrepositionalNeuter(self):
        self.assertIn('э́том', self.pronoun.prepositional.neuter)

    def testCanParsePrepositinalFeminine(self):
        self.assertIn('э́той', self.pronoun.prepositional.feminine)

    def testCanParsePrepositinalPlural(self):
        self.assertIn('э́тих', self.pronoun.prepositional.plural)