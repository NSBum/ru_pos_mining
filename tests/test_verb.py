import unittest
from grammar import *
from ruwiktionary import *


class TestVerbTense(unittest.TestCase):
    def testCanAddSingularFormFirstPerson(self):
        vt = VerbTense()
        vt.add_form_issingular(True, 'dog', 1)
        self.assertTrue(vt.singular.p1 == 'dog')

    def testCanAddSingularFormSecondPerson(self):
        vt = VerbTense()
        vt.add_form_issingular(True, 'cat', 2)
        self.assertTrue(vt.singular.p2 == 'cat')

    def testCanAddSingularFormThirdPerson(self):
        vt = VerbTense()
        vt.add_form_issingular(True, 'moose', 3)
        self.assertTrue(vt.singular.p3 == 'moose')

    def testCanAddPluralFormFirstPerson(self):
        vt = VerbTense()
        vt.add_form_issingular(False, 'dog', 1)
        self.assertTrue(vt.plural.p1 == 'dog')

    def testCanAddPluralFormSecondPerson(self):
        obj = VerbTense()
        obj.add_form_issingular(False, 'cat', 2)
        self.assertTrue(obj.plural.p2 == 'cat')

    def testCanAddPluralFormThirdPerson(self):
        obj = VerbTense()
        obj.add_form_issingular(False, 'moose', 3)
        self.assertTrue(obj.plural.p3 == 'moose')

    def formList(self):
        return ['a', 'b', 'c', 'd', 'e', 'f']

    def testSetForms(self):
        obj = VerbTense()
        obj.add_form_list(self.formList())
        self.assertTrue(obj.singular.p1 == 'a')
        self.assertTrue(obj.singular.p2 == 'b')
        self.assertTrue(obj.singular.p3 == 'c')
        self.assertTrue(obj.plural.p1 == 'd')
        self.assertTrue(obj.plural.p2 == 'e')
        self.assertTrue(obj.plural.p3 == 'f')

    def testGetFormByString(self):
        obj = VerbTense()
        obj.add_form_list(self.formList())
        self.assertTrue(obj.getform_for_numberstr_personstr('singular', 'p1') == 'a')
        self.assertTrue(obj.getform_for_numberstr_personstr('singular', 'p2') == 'b')
        self.assertTrue(obj.getform_for_numberstr_personstr('singular', 'p3') == 'c')
        self.assertTrue(obj.getform_for_numberstr_personstr('plural', 'p1') == 'd')
        self.assertTrue(obj.getform_for_numberstr_personstr('plural', 'p2') == 'e')
        self.assertTrue(obj.getform_for_numberstr_personstr('plural', 'p3') == 'f')


class TestVerb(unittest.TestCase):
    def testEmptyVerbHasNoPresentTense(self):
        self.assertFalse(Verb('test').has_present_tense())

    def testEmptyVerbHasNoFutureTense(self):
        self.assertFalse(Verb('test').has_future_tense())

    def testEmptyVerbHasNoPastTense(self):
        self.assertFalse(Verb('test').has_tense_named('past'))

    def testEmptyVerbHasNoImperativeTense(self):
        self.assertFalse(Verb('test').has_tense_named('imperative'))


class TestVerbPastTense(unittest.TestCase):
    def setUp(self) -> None:
        self.verb: Verb = Verb('dog')
        self.verb.add_past_form('testm', 'masculine')
        self.verb.add_past_form('testf', 'feminine')
        self.verb.add_past_form('testn', 'neuter')
        self.verb.add_past_form('testp', 'plural')

    def tearDown(self) -> None:
        self.verb = None

    def testPastMasculineInflectionCode(self):
        code_tuples = self.verb.inflection_code_list
        codes = [x[1] for x in code_tuples]
        self.assertIn(302, codes)

    def testPastFeminineInflectionCode(self):
        code_tuples = self.verb.inflection_code_list
        codes = [x[1] for x in code_tuples]
        self.assertIn(303, codes)

    def testPastNeuterInflectionCode(self):
        code_tuples = self.verb.inflection_code_list
        codes = [x[1] for x in code_tuples]
        self.assertIn(304, codes)

    def testPastPluralInflectionCode(self):
        code_tuples = self.verb.inflection_code_list
        codes = [x[1] for x in code_tuples]
        self.assertIn(304, codes)


class TestVerbInflectionCodes(unittest.TestCase):
    def setUp(self) -> None:
        self.verb = Verb('test')

    def tearDown(self) -> None:
        self.verb = None

    def code_list(self):
        code_tuples = self.verb.inflection_code_list
        codes = [x[1] for x in code_tuples]
        return codes

    def form_in_code_list_for_code(self, code):
        code_tuples = self.verb.inflection_code_list
        forms = [x[0] for x in code_tuples if x[1] == code]
        if forms:
            return forms[0]
        else:
            return None


class TestVerbPresentTenseInflectionCodes(unittest.TestCase):
    def setUp(self) -> None:
        self.verb = Verb('test')
        self.verb.present.add_form_list(['a', 'b', 'c', 'd', 'e', 'f'])

    def tearDown(self) -> None:
        self.verb = None

    def code_list(self):
        code_tuples = self.verb.inflection_code_list
        codes = [x[1] for x in code_tuples]
        return codes

    def form_in_code_list_for_code(self, code):
        code_tuples = self.verb.inflection_code_list
        forms = [x[0] for x in code_tuples if x[1] == code]
        if forms:
            return forms[0]
        else:
            return None

    def testFirstPersonSingularCode(self):
        self.assertIn(306, self.code_list())
        self.assertEqual('a', self.form_in_code_list_for_code(306))

    def testSecondPersonSingularCode(self):
        self.assertEqual('b', self.form_in_code_list_for_code(307))

    def testThirdPersonSingularCode(self):
        self.assertEqual('c', self.form_in_code_list_for_code(308))

    def testFirstPersonPluralCode(self):
        self.assertIn(306, self.code_list())
        self.assertEqual('d', self.form_in_code_list_for_code(309))

    def testSecondPersonPluralCode(self):
        self.assertEqual('e', self.form_in_code_list_for_code(310))

    def testThirdPersonPluralCode(self):
        self.assertEqual('f', self.form_in_code_list_for_code(311))


class TestVerbFutureTenseInflectionCodes(unittest.TestCase):
    def setUp(self) -> None:
        self.verb = Verb('test')
        self.verb.future.add_form_list(['a', 'b', 'c', 'd', 'e', 'f'])

    def tearDown(self) -> None:
        self.verb = None

    def code_list(self):
        code_tuples = self.verb.inflection_code_list
        codes = [x[1] for x in code_tuples]
        return codes

    def form_in_code_list_for_code(self, code):
        code_tuples = self.verb.inflection_code_list
        forms = [x[0] for x in code_tuples if x[1] == code]
        if forms:
            return forms[0]
        else:
            return None

    def testFirstPersonSingularCode(self):
        self.assertEqual('a', self.form_in_code_list_for_code(312))

    def testSecondPersonSingularCode(self):
        self.assertEqual('b', self.form_in_code_list_for_code(313))

    def testThirdPersonSingularCode(self):
        self.assertEqual('c', self.form_in_code_list_for_code(314))

    def testFirstPersonPluralCode(self):
        self.assertEqual('d', self.form_in_code_list_for_code(315))

    def testSecondPersonPluralCode(self):
        self.assertEqual('e', self.form_in_code_list_for_code(316))

    def testThirdPersonPluralCode(self):
        self.assertEqual('f', self.form_in_code_list_for_code(317))


class TestVerbImperativeTenseInflectionCodes(unittest.TestCase):
    def setUp(self) -> None:
        self.verb = Verb('test')
        self.verb.imperative.singular = 'a'
        self.verb.imperative.plural = 'b'

    def tearDown(self) -> None:
        self.verb = None

    def code_list(self):
        code_tuples = self.verb.inflection_code_list
        codes = [x[1] for x in code_tuples]
        return codes

    def form_in_code_list_for_code(self, code):
        code_tuples = self.verb.inflection_code_list
        forms = [x[0] for x in code_tuples if x[1] == code]
        if forms:
            return forms[0]
        else:
            return None

    def testSingularImperativeTenseInflectionCode(self):
        self.assertEqual('a', self.form_in_code_list_for_code(300))

    def testPluralImperativeTenseInflectionCode(self):
        self.assertEqual('b', self.form_in_code_list_for_code(301))


class TestPresentActiveParticiple(TestVerbInflectionCodes):
    def testPresentActiveParticipleInflectionCode(self):
        self.verb.present_active_participle = 'testp'
        self.assertEqual('testp', self.form_in_code_list_for_code(318))


class TestPastActiveParticiple(TestVerbInflectionCodes):
    def testPastActiveParticipleInflectionCode(self):
        self.verb.past_active_participle = 'testp2'
        self.assertEqual('testp2', self.form_in_code_list_for_code(319))


class TestPresentPassiveParticiple(TestVerbInflectionCodes):
    def testPresentPassiveParticiple(self):
        self.verb.present_passive_participle = 'testp3'
        self.assertEqual('testp3', self.form_in_code_list_for_code(322))


class TestPastPassiveParticiple(TestVerbInflectionCodes):
    def testPastPassiveParticiple(self):
        self.verb.past_passive_participle = 'testp4'
        self.assertEqual('testp4', self.form_in_code_list_for_code(323))


class TestPresentAdverbialParticiple(TestVerbInflectionCodes):
    def testPresentAdverbialParticiple(self):
        self.verb.present_adverbial_participle = 'testp5'
        self.assertEqual('testp5', self.form_in_code_list_for_code(320))


class TestPastAdverbialParticiple(TestVerbInflectionCodes):
    def testPastAdverbialParticiple(self):
        form = 'testp6'
        self.verb.past_adverbial_participle = [form]
        self.assertEqual(form, self.form_in_code_list_for_code(321))


class TestParsePerfectiveVerb(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = RuWikitionary('отсидеть', True, 'verb_pf_отсидеть.html')
        cls.verb = cls.page.parse_verb()

    def testThatPageIsSet(self):
        self.assertIsNotNone(self.page)

    def testCanParsePage(self):
        self.assertIsNotNone(self.page.root_tree)

    def testCanParseVerb(self):
        self.assertIsNotNone(self.verb)

    def testCanParseFirstPersonSingularFuture(self):
        actual = self.verb.future.singular.p1
        self.assertEqual(actual, 'отсижу́')

    def testCanParseFirstPersonPluralFuture(self):
        actual = self.verb.future.plural.p1
        self.assertEqual(actual, 'отсиди́м')

    def testCanParseSecondPersonSingularFuture(self):
        actual = self.verb.future.singular.p2
        self.assertEqual(actual, 'отсиди́шь')

    def testCanParseSecondPersonPluralFuture(self):
        actual = self.verb.future.plural.p2
        self.assertEqual(actual, 'отсиди́те')

    def testCanParseThirdPersonSingularFuture(self):
        actual = self.verb.future.singular.p3
        self.assertEqual(actual, 'отсиди́т')

    def testCanParseThirdPersonPluralFuture(self):
        actual = self.verb.future.plural.p3
        self.assertEqual(actual, 'отсидя́т')

    def testCanParsePastTenseMasculine(self):
        actual = self.verb.past.masculine
        self.assertEqual(actual, 'отсиде́л')

    def testCanParsePastTenseFeminine(self):
        actual = self.verb.past.feminine
        self.assertEqual(actual, 'отсиде́ла')

    def testCanParsePastTenseNeuter(self):
        actual = self.verb.past.neuter
        self.assertEqual(actual, 'отсиде́ло')

    def testCanParsePastTensePlural(self):
        actual = self.verb.past.plural
        self.assertEqual(actual, 'отсиде́ли')

    def testCanParseImperativeSingular(self):
        actual = self.verb.imperative.singular
        self.assertEqual(actual, 'отсиди́')

    def testCanParseImperativePlural(self):
        actual = self.verb.imperative.plural
        self.assertEqual(actual, 'отсиди́те')

    def testCanParsePastActiveParticiple(self):
        actual = self.verb.past_active_participle
        self.assertEqual(actual, 'отсиде́вший')

    def testCanParsePastAdverbialParticiple(self):
        # отсиде́в, отсиде́вши
        actual = self.verb.past_adverbial_participle
        self.assertIn('отсиде́в', actual)
        self.assertIn('отсиде́вши', actual)

    def testCanParsePastPassiveParticiple(self):
        actual = self.verb.past_passive_participle
        self.assertEqual(actual, 'отси́женный')


class TestParsePerfectiveVerbB(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = RuWikitionary('сделать', True, 'verb_pf_сделать.html')
        cls.verb = cls.page.parse_verb()

    def testThatPageIsSet(self):
        self.assertIsNotNone(self.page)

    def testCanParsePage(self):
        self.assertIsNotNone(self.page.root_tree)

    def testCanParseVerb(self):
        self.assertIsNotNone(self.verb)

    def testCanParseFirstPersonSingularFuture(self):
        actual = self.verb.future.singular.p1
        self.assertEqual(actual, 'сде́лаю')

    def testCanParseFirstPersonPluralFuture(self):
        actual = self.verb.future.plural.p1
        self.assertEqual(actual, 'сде́лаем')

    def testCanParseSecondPersonSingularFuture(self):
        actual = self.verb.future.singular.p2
        self.assertEqual(actual, 'сде́лаешь')

    def testCanParseSecondPersonPluralFuture(self):
        actual = self.verb.future.plural.p2
        self.assertEqual(actual, 'сде́лаете')

    def testCanParseThirdPersonSingularFuture(self):
        actual = self.verb.future.singular.p3
        self.assertEqual(actual, 'сде́лает')

    def testCanParseThirdPersonPluralFuture(self):
        actual = self.verb.future.plural.p3
        self.assertEqual(actual, 'сде́лают')

    def testCanParsePastTenseMasculine(self):
        actual = self.verb.past.masculine
        self.assertEqual(actual, 'сде́лал')

    def testCanParsePastTenseFeminine(self):
        actual = self.verb.past.feminine
        self.assertEqual(actual, 'сде́лала')

    def testCanParsePastTenseNeuter(self):
        actual = self.verb.past.neuter
        self.assertEqual(actual, 'сде́лало')

    def testCanParsePastTensePlural(self):
        actual = self.verb.past.plural
        self.assertEqual(actual, 'сде́лали')

    def testCanParseImperativeSingular(self):
        actual = self.verb.imperative.singular
        self.assertEqual(actual, 'сде́лай')

    def testCanParseImperativePlural(self):
        actual = self.verb.imperative.plural
        self.assertEqual(actual, 'сде́лайте')

    def testCanParsePastActiveParticiple(self):
        actual = self.verb.past_active_participle
        self.assertEqual(actual, 'сде́лавший')

    def testCanParsePastAdverbialParticiple(self):
        # сде́лав, сде́лавши
        actual = self.verb.past_adverbial_participle
        self.assertIn('сде́лав', actual)
        self.assertIn('сде́лавши', actual)

    def testCanParsePastPassiveParticiple(self):
        actual = self.verb.past_passive_participle
        self.assertEqual(actual, 'сде́ланный')


class TestParseImperfectiveVerbA(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = RuWikitionary('делать', True, 'verb_ipf_делать.html')
        cls.verb = cls.page.parse_verb()

    def testThatPageIsSet(self):
        self.assertIsNotNone(self.page)

    def testCanParsePage(self):
        self.assertIsNotNone(self.page.root_tree)

    def testCanParseVerb(self):
        self.assertIsNotNone(self.verb)

    def testCanParseFirstPersonSingularPresent(self):
        actual = self.verb.present.singular.p1
        self.assertEqual(actual, 'де́лаю')

    def testCanParseFirstPersonPluralPresent(self):
        actual = self.verb.present.plural.p1
        self.assertEqual(actual, 'де́лаем')

    def testCanParseSecondPersonSingularPresent(self):
        actual = self.verb.present.singular.p2
        self.assertEqual(actual, 'де́лаешь')

    def testCanParseSecondPersonPluralPresent(self):
        actual = self.verb.present.plural.p2
        self.assertEqual(actual, 'де́лаете')

    def testCanParseThirdPersonSingularPresent(self):
        actual = self.verb.present.singular.p3
        self.assertEqual(actual, 'де́лает')

    def testCanParseThirdPersonPluralPresent(self):
        actual = self.verb.present.plural.p3
        self.assertEqual(actual, 'де́лают')

    def testCanParsePastTenseMasculine(self):
        actual = self.verb.past.masculine
        self.assertEqual(actual, 'де́лал')

    def testCanParsePastTenseFeminine(self):
        actual = self.verb.past.feminine
        self.assertEqual(actual, 'де́лала')

    def testCanParsePastTenseNeuter(self):
        actual = self.verb.past.neuter
        self.assertEqual(actual, 'де́лало')

    def testCanParsePastTensePlural(self):
        actual = self.verb.past.plural
        self.assertEqual(actual, 'де́лали')

    def testCanParseImperativeSingular(self):
        actual = self.verb.imperative.singular
        self.assertEqual(actual, 'де́лай')

    def testCanParseImperativePlural(self):
        actual = self.verb.imperative.plural
        self.assertEqual(actual, 'де́лайте')

    def testCanParsePastActiveParticiple(self):
        actual = self.verb.past_active_participle
        self.assertEqual(actual, 'де́лавший')

    def testCanParsePastAdverbialParticiple(self):
        # сде́лав, сде́лавши
        actual = self.verb.past_adverbial_participle
        self.assertIn('де́лав', actual)
        self.assertIn('де́лавши', actual)

    def testCanParsePastPassiveParticiple(self):
        actual = self.verb.past_passive_participle
        self.assertEqual(actual, 'де́ланный')

    def testCanParsePresentPassiveParticiple(self):
        actual = self.verb.present_passive_participle
        self.assertEqual(actual, 'де́лаемый')

    def testCanParsePresentAdverbialParticiple(self):
        actual = self.verb.present_adverbial_participle
        self.assertEqual(actual, 'де́лая')


class TestParseImperfectiveVerbB(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = RuWikitionary('идти', True, 'verb_ipf_идти.html')
        cls.verb = cls.page.parse_verb()

    def testThatPageIsSet(self):
        self.assertIsNotNone(self.page)

    def testCanParsePage(self):
        self.assertIsNotNone(self.page.root_tree)

    def testCanParseVerb(self):
        self.assertIsNotNone(self.verb)

    def testCanExtractSpeechPart(self):
        self.assertEqual(self.page.pos, SpeechPart.VERB)

    def testCanParseFirstPersonSingularPresent(self):
        actual = self.verb.present.singular.p1
        self.assertEqual(actual, 'иду́')

    def testCanParseFirstPersonPluralPresent(self):
        actual = self.verb.present.plural.p1
        self.assertEqual(actual, 'идём')

    def testCanParseSecondPersonSingularPresent(self):
        actual = self.verb.present.singular.p2
        self.assertEqual(actual, 'идёшь')

    def testCanParseSecondPersonPluralPresent(self):
        actual = self.verb.present.plural.p2
        self.assertEqual(actual, 'идёте')

    def testCanParseThirdPersonSingularPresent(self):
        actual = self.verb.present.singular.p3
        self.assertEqual(actual, 'идёт')

    def testCanParseThirdPersonPluralPresent(self):
        actual = self.verb.present.plural.p3
        self.assertEqual(actual, 'иду́т')

    def testCanParsePastTenseMasculine(self):
        actual = self.verb.past.masculine
        self.assertEqual(actual, 'шёл')

    def testCanParsePastTenseFeminine(self):
        actual = self.verb.past.feminine
        self.assertEqual(actual, 'шла́')

    def testCanParsePastTenseNeuter(self):
        actual = self.verb.past.neuter
        self.assertEqual(actual, 'шло́')

    def testCanParsePastTensePlural(self):
        actual = self.verb.past.plural
        self.assertEqual(actual, 'шли́')

    def testCanParseImperativeSingular(self):
        actual = self.verb.imperative.singular
        self.assertEqual(actual, 'иди́')

    def testCanParseImperativePlural(self):
        actual = self.verb.imperative.plural
        self.assertEqual(actual, 'иди́те')

    def testCanParsePastActiveParticiple(self):
        actual = self.verb.past_active_participle
        self.assertEqual(actual, 'ше́дший')

    def testCanParsePastAdverbialParticiple(self):
        # сде́лав, сде́лавши
        actual = self.verb.past_adverbial_participle
        self.assertIn('ше́дши', actual)

    def testCanParsePastPassiveParticiple(self):
        actual = self.verb.past_passive_participle
        self.assertIsNone(actual)

    def testCanParsePresentPassiveParticiple(self):
        actual = self.verb.present_passive_participle
        self.assertIsNone(actual)

    def testCanParsePresentAdverbialParticiple(self):
        actual = self.verb.present_adverbial_participle
        self.assertEqual(actual, 'идя́')

    def testCanParsePresentActiveParticiple(self):
        actual = self.verb.present_active_participle
        self.assertEqual(actual, 'иду́щий')