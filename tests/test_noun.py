import unittest
from grammar import *
from ruwiktionary import *


class TestNounAddForm(unittest.TestCase):
    def setUp(self) -> None:
        self.noun = Noun('test')

    def tearDown(self) -> None:
        self.noun = None

    def testAddNotListRaises(self):
        with self.assertRaises(ValueError):
            self.noun.add_form_case_name('nominative', True, 'testm')

    def testAddNominativeSingular(self):
        self.noun.add_form_case_name('nominative', True, ['testn'])
        self.assertIn('testn', self.noun.nominative.singular)

    def testAddNominativePlural(self):
        self.noun.add_form_case_name('nominative', False, ['testn1'])
        self.assertIn('testn1', self.noun.nominative.plural)

    def testAddGenitiveSingular(self):
        self.noun.add_form_case_name('genitive', True, ['testg'])
        self.assertIn('testg', self.noun.genitive.singular)

    def testAddGenitivePlural(self):
        self.noun.add_form_case_name('genitive', False, ['testg1'])
        self.assertIn('testg1', self.noun.genitive.plural)

    def testAddDativeSingular(self):
        form = 'testd'
        self.noun.add_form_case_name('dative', True, [form])
        self.assertIn(form, self.noun.dative.singular)

    def testAddDativePlural(self):
        form = 'testd1'
        self.noun.add_form_case_name('dative', False, [form])
        self.assertIn(form, self.noun.dative.plural)

    def testAddAccusativeSingular(self):
        form = 'testa'
        self.noun.add_form_case_name('accusative', True, [form])
        self.assertIn(form, self.noun.accusative.singular)

    def testAddAccusativePlural(self):
        form = 'testa1'
        self.noun.add_form_case_name('accusative', False, [form])
        self.assertIn(form, self.noun.accusative.plural)

    def testAddInstrumentalSingular(self):
        form = 'testi'
        self.noun.add_form_case_name('instrumental', True, [form])
        self.assertIn(form, self.noun.instrumental.singular)

    def testAddInstrumentalPlural(self):
        form = 'testi1'
        self.noun.add_form_case_name('instrumental', False, [form])
        self.assertIn(form, self.noun.instrumental.plural)

    def testAddPrepositionalSingular(self):
        form = 'testp'
        self.noun.add_form_case_name('prepositional', True, [form])
        self.assertIn(form, self.noun.prepositional.singular)

    def testAddPrepositionalPlural(self):
        form = 'testp1'
        self.noun.add_form_case_name('prepositional', False, [form])
        self.assertIn(form, self.noun.prepositional.plural)

    def testAddLocativeSingular(self):
        form = 'testl'
        self.noun.add_form_case_name('locative', True, [form])
        self.assertIn(form, self.noun.locative.singular)

    def testAddLocativePlural(self):
        form = 'testl1'
        self.noun.add_form_case_name('locative', False, [form])
        self.assertIn(form, self.noun.locative.plural)

    def testAddVocativeSingular(self):
        form = 'testv'
        self.noun.add_form_case_name('vocative', True, [form])
        self.assertIn(form, self.noun.vocative.singular)

    def testAddVocativePlural(self):
        form = 'testv1'
        self.noun.add_form_case_name('vocative', False, [form])
        self.assertIn(form, self.noun.vocative.plural)


class TestNounInflectionCodes(unittest.TestCase):
    def setUp(self) -> None:
        self.noun = Noun('test')

    def tearDown(self) -> None:
        self.noun = None

    def code_list(self):
        code_tuples = self.noun.inflection_code_list
        codes = [x[1] for x in code_tuples]
        return codes

    def form_in_code_list_for_code(self, code):
        code_tuples = self.noun.inflection_code_list
        forms = [x[0] for x in code_tuples if x[1] == code]
        if forms:
            return forms[0]
        else:
            return None


class TestNounNominativeInflectionCodes(TestNounInflectionCodes):
    def setUp(self) -> None:
        super().setUp()
        self.noun.add_form_case_name('nominative', True, ['nsing'])
        self.noun.add_form_case_name('nominative', False, ['nplur'])

    def testNominativeSingularInflectionCode(self):
        self.assertEqual('nsing', self.form_in_code_list_for_code(1))

    def testNominativePluralInflectionCode(self):
        self.assertEqual('nplur', self.form_in_code_list_for_code(2))


class TestNounGenitiveInflectionCodes(TestNounInflectionCodes):
    def setUp(self) -> None:
        super().setUp()
        self.noun.add_form_case_name('genitive', True, ['gsing'])
        self.noun.add_form_case_name('genitive', False, ['gplur'])

    def testNominativeSingularInflectionCode(self):
        self.assertEqual('gsing', self.form_in_code_list_for_code(3))

    def testNominativePluralInflectionCode(self):
        self.assertEqual('gplur', self.form_in_code_list_for_code(4))


class TestNounDativeInflectionCodes(TestNounInflectionCodes):
    def setUp(self) -> None:
        super().setUp()
        self.noun.add_form_case_name('dative', True, ['dsing'])
        self.noun.add_form_case_name('dative', False, ['dplur'])

    def testDativeSingularInflectionCode(self):
        self.assertEqual('dsing', self.form_in_code_list_for_code(7))

    def testDativePluralInflectionCode(self):
        self.assertEqual('dplur', self.form_in_code_list_for_code(8))


class TestNounAccusativeInflectionCodes(TestNounInflectionCodes):
    def setUp(self) -> None:
        super().setUp()
        self.noun.add_form_case_name('accusative', True, ['asing'])
        self.noun.add_form_case_name('accusative', False, ['aplur'])

    def testDativeSingularInflectionCode(self):
        self.assertEqual('asing', self.form_in_code_list_for_code(5))

    def testDativePluralInflectionCode(self):
        self.assertEqual('aplur', self.form_in_code_list_for_code(6))


class TestNounInstrumentalInflectionCodes(TestNounInflectionCodes):
    def setUp(self) -> None:
        super().setUp()
        self.noun.add_form_case_name('instrumental', True, ['ising'])
        self.noun.add_form_case_name('instrumental', False, ['iplur'])

    def testInstrumentalSingularInflectionCode(self):
        self.assertEqual('ising', self.form_in_code_list_for_code(9))

    def testInstrumentalPluralInflectionCode(self):
        self.assertEqual('iplur', self.form_in_code_list_for_code(11))


class TestNounPrepositionalInflectionCodes(TestNounInflectionCodes):
    def setUp(self) -> None:
        super().setUp()
        self.noun.add_form_case_name('prepositional', True, ['psing'])
        self.noun.add_form_case_name('prepositional', False, ['pplur'])

    def testPrepositionalSingularInflectionCode(self):
        self.assertEqual('psing', self.form_in_code_list_for_code(12))

    def testPrepositionalPluralInflectionCode(self):
        self.assertEqual('pplur', self.form_in_code_list_for_code(14))


class TestNounLocativeInflectionCodes(TestNounInflectionCodes):
    def setUp(self) -> None:
        super().setUp()
        self.sform = 'lsing'
        self.noun.add_form_case_name('locative', True, [self.sform])

    def testLocativeSingularInflectionCode(self):
        self.assertEqual(self.sform, self.form_in_code_list_for_code(17))


class TestNounVocativeInflectionCodes(TestNounInflectionCodes):
    def setUp(self) -> None:
        super().setUp()
        self.sform = 'vsing'

        self.noun.add_form_case_name('vocative', True, [self.sform])

    def testVocativeSingularInflectionCode(self):
        self.assertEqual(self.sform, self.form_in_code_list_for_code(15))


class TestCanParseNounA(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = RuWikitionary('дошколница', True, 'noun_sample_01.html')
        cls.noun: Noun = cls.page.parse_noun()

    def testThatPageIsSet(self):
        self.assertIsNotNone(self.page)

    def testCanParsePage(self):
        self.assertIsNotNone(self.page.root_tree)

    def testCanExtractSpeechPart(self):
        self.assertEqual(self.page.pos, SpeechPart.NOUN)

    def testCanParseNominativeSingular(self):
        actual = self.noun.nominative.singular
        self.assertIn('дошко́льница', actual)

    def testCanParseNominativePlural(self):
        actual = self.noun.nominative.plural
        self.assertIn('дошко́льницы', actual)

    def testCanParseGenitiveSingular(self):
        actual = self.noun.genitive.singular
        self.assertIn('дошко́льницы', actual)

    def testCanParseGenitivePlural(self):
        actual = self.noun.genitive.plural
        self.assertIn('дошко́льниц', actual)

    def testCanParseDativeSingular(self):
        actual = self.noun.dative.singular
        self.assertIn('дошко́льнице', actual)

    def testCanParseDativePlural(self):
        actual = self.noun.dative.plural
        self.assertIn('дошко́льницам', actual)

    def testCanParseAccusativeSingular(self):
        actual = self.noun.accusative.singular
        self.assertIn('дошко́льницу', actual)

    def testCanParseAccusativePlural(self):
        actual = self.noun.accusative.plural
        self.assertIn('дошко́льниц', actual)

    def testCanParseInstrumentalSingular(self):
        actual = self.noun.instrumental.singular
        self.assertIn('дошко́льницей', actual)
        self.assertIn('дошко́льницею', actual)

    def testCanParseInstrumentalPlural(self):
        actual = self.noun.instrumental.plural
        self.assertIn('дошко́льницами', actual)

    def testCanParsePrepositionalSingular(self):
        actual = self.noun.prepositional.singular
        self.assertIn('дошко́льнице', actual)

    def testCanParsePrepositionalPlural(self):
        actual = self.noun.prepositional.plural
        self.assertIn('дошко́льницах', actual)


class TestCanParseNounNeuterA(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = RuWikitionary('отсутствие', True, 'noun_neuter_отсутствие.html')
        cls.noun: Noun = cls.page.parse_noun()

    def testThatPageIsSet(self):
        self.assertIsNotNone(self.page)

    def testCanParsePage(self):
        self.assertIsNotNone(self.page.root_tree)

    def testCanParseNominativeSingular(self):
        actual = self.noun.nominative.singular
        self.assertIn('отсу́тствие', actual)

    def testCanParseNominativePlural(self):
        actual = self.noun.nominative.plural
        self.assertIn('отсу́тствия', actual)

    def testCanParseGenitiveSingular(self):
        actual = self.noun.genitive.singular
        self.assertIn('отсу́тствия', actual)

    def testCanParseGenitivePlural(self):
        actual = self.noun.genitive.plural
        self.assertIn('отсу́тствий', actual)

    def testCanParseDativeSingular(self):
        actual = self.noun.dative.singular
        self.assertIn('отсу́тствию', actual)

    def testCanParseDativePlural(self):
        actual = self.noun.dative.plural
        self.assertIn('отсу́тствиям', actual)

    def testCanParseAccusativeSingular(self):
        actual = self.noun.accusative.singular
        self.assertIn('отсу́тствие', actual)

    def testCanParseAccusativePlural(self):
        actual = self.noun.accusative.plural
        self.assertIn('отсу́тствия', actual)

    def testCanParseInstrumentalSingular(self):
        actual = self.noun.instrumental.singular
        self.assertIn('отсу́тствием', actual)

    def testCanParseInstrumentalPlural(self):
        actual = self.noun.instrumental.plural
        self.assertIn('отсу́тствиями', actual)

    def testCanParsePrepositionalSingular(self):
        actual = self.noun.prepositional.singular
        self.assertIn('отсу́тствии', actual)

    def testCanParsePrepositionalPlural(self):
        actual = self.noun.prepositional.plural
        self.assertIn('отсу́тствиях', actual)


class TestCanParseNounMasculineA(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = RuWikitionary('магазин', True, 'noun_masculine_магазин.html')
        cls.noun: Noun = cls.page.parse_noun()

    def testThatPageIsSet(self):
        self.assertIsNotNone(self.page)

    def testCanParsePage(self):
        self.assertIsNotNone(self.page.root_tree)

    def testCanParseNominativeSingular(self):
        actual = self.noun.nominative.singular
        self.assertIn('магази́н', actual)

    def testCanParseNominativePlural(self):
        actual = self.noun.nominative.plural
        self.assertIn('магази́ны', actual)

    def testCanParseGenitiveSingular(self):
        actual = self.noun.genitive.singular
        self.assertIn('магази́на', actual)

    def testCanParseGenitivePlural(self):
        actual = self.noun.genitive.plural
        self.assertIn('магази́нов', actual)

    def testCanParseDativeSingular(self):
        actual = self.noun.dative.singular
        self.assertIn('магази́ну', actual)

    def testCanParseDativePlural(self):
        actual = self.noun.dative.plural
        self.assertIn('магази́нам', actual)

    def testCanParseAccusativeSingular(self):
        actual = self.noun.accusative.singular
        self.assertIn('магази́н', actual)

    def testCanParseAccusativePlural(self):
        actual = self.noun.accusative.plural
        self.assertIn('магази́ны', actual)

    def testCanParseInstrumentalSingular(self):
        actual = self.noun.instrumental.singular
        self.assertIn('магази́ном', actual)

    def testCanParseInstrumentalPlural(self):
        actual = self.noun.instrumental.plural
        self.assertIn('магази́нами', actual)

    def testCanParsePrepositionalSingular(self):
        actual = self.noun.prepositional.singular
        self.assertIn('магази́не', actual)

    def testCanParsePrepositionalPlural(self):
        actual = self.noun.prepositional.plural
        self.assertIn('магази́нах', actual)


class TestCanParseNounFeminineB(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = RuWikitionary('собака', True, 'noun_feminine_собака.html')
        cls.noun: Noun = cls.page.parse_noun()

    def testThatPageIsSet(self):
        self.assertIsNotNone(self.page)

    def testCanParsePage(self):
        self.assertIsNotNone(self.page.root_tree)

    def testCanExtractSpeechPart(self):
        self.assertEqual(self.page.pos, SpeechPart.NOUN)

    def testCanParseNominativeSingular(self):
        actual = self.noun.nominative.singular
        self.assertIn('соба́ка', actual)

    def testCanParseInstrumentalSingular(self):
        actual = self.noun.instrumental.singular
        self.assertIn('соба́кой', actual)
        self.assertIn('соба́кою', actual)

    def testCanParseInstrumentalPlural(self):
        actual = self.noun.instrumental.plural
        self.assertIn('соба́ками', actual)
