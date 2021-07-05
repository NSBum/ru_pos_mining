import unittest
from grammar import *


class TestGrammarProperties(unittest.TestCase):
    def nothing(self):
        self.assertTrue(True)

    def attributeInObjectProps(self, attr, obj):
        self.assertTrue(attr in obj.__dir__())

    def attributeNotInObjectProps(self, attr, obj):
        self.assertFalse(attr in obj.__dir__())

    def testVerbImperativeTenseHasSingularAttribute(self):
        props = VerbImperativeTense().__dir__()
        self.assertTrue('singular' in props)

    def testVerbImperativeTenseHasPluralAttribute(self):
        props = VerbImperativeTense().__dir__()
        self.assertTrue('plural' in props)

    def testVerbImperativeTenseHasNominativeAttribute(self):
        props = VerbImperativeTense().__dir__()
        self.assertFalse('nominative' in props)

    def testVerbPastTenseHasMasculineAttribute(self):
        self.attributeInObjectProps('masculine', VerbPastTense())

    def testVerbPastTenseHasFeminineAttribute(self):
        self.attributeInObjectProps('feminine', VerbPastTense())

    def testVerbPastTenseHasNeuterAttribute(self):
        self.attributeInObjectProps('neuter', VerbPastTense())

    def testVerbPastTenseHasPluralAttribute(self):
        self.attributeInObjectProps('plural', VerbPastTense())

    def testVerbPastTenseHasSingularAttribute(self):
        self.attributeNotInObjectProps('singular', VerbPastTense())


class TestRussianPOSTranslation(unittest.TestCase):
    def testRussianPOSTRanslationNoun(self):
        case = 'существительное'
        self.assertTrue(rupos2upos(case) == 'NOUN')


class TestNounCaseType2Name(unittest.TestCase):
    def testNominative2NominativeCaseType(self):
        self.assertEqual('nominative', NounCaseType.case_name_for_type(NounCaseType.NOMINATIVE))

    def testNominative2GenitiveCaseType(self):
        self.assertEqual('genitive', NounCaseType.case_name_for_type(NounCaseType.GENITIVE))

    def testNominative2DativeCaseType(self):
        self.assertEqual('dative', NounCaseType.case_name_for_type(NounCaseType.DATIVE))

    def testNominative2AccusativeCaseType(self):
        self.assertEqual('accusative', NounCaseType.case_name_for_type(NounCaseType.ACCUSATIVE))

    def testNominative2InstrumentalCaseType(self):
        self.assertEqual('instrumental', NounCaseType.case_name_for_type(NounCaseType.INSTRUMENTAL))

    def testNominative2PrepositionalCaseType(self):
        self.assertEqual('prepositional', NounCaseType.case_name_for_type(NounCaseType.PREPOSITIONAL))

    def testNominative2LocativeCaseType(self):
        self.assertEqual('locative', NounCaseType.case_name_for_type(NounCaseType.LOCATIVE))

    def testNominative2VocativeCaseType(self):
        self.assertEqual('vocative', NounCaseType.case_name_for_type(NounCaseType.VOCATIVE))


class TestInflectionCodes(unittest.TestCase):
    def testCanLoadInflectionCodes(self):
        with open('inflection_codes.yaml') as file:
            inflection_codes = yaml.safe_load(file)
        self.assertIsNotNone(inflection_codes)


class TestSpeechPart2UPOS(unittest.TestCase):
    def testSpeechPartNOUN2NOUN(self):
        self.assertEqual(SpeechPart.NOUN.to_upos(), 'NOUN')

    def testSpeechPartADJECTIVE2ADJ(self):
        self.assertEqual(SpeechPart.ADJECTIVE.to_upos(), 'ADJ')

    def testSpeechPartADVERB2ADV(self):
        self.assertEqual(SpeechPart.ADVERB.to_upos(), 'ADV')

    def testSpeechPartVERB2VERB(self):
        self.assertEqual(SpeechPart.VERB.to_upos(), 'VERB')

    def testSpeechPartPossessivePronoun2PRON(self):
        self.assertEqual(SpeechPart.PRONOUN_POSSESSIVE.to_upos(), 'PRON')

    def testSpeechPartPRONOUN2PRON(self):
        self.assertEqual(SpeechPart.PRONOUN.to_upos(), 'PRON')

    def testSpeechPartPREPOSITION2ADP(self):
        self.assertEqual(SpeechPart.PREPOSITION.to_upos(), 'ADP')

    def testSpeechPartNUMERAL2NUM(self):
        self.assertEqual(SpeechPart.NUMERAL.to_upos(), 'NUM')


class TestCodeToTerm(unittest.TestCase):
    def testCode400(self):
        self.assertEqual(code2term(400), 'possessive pronoun, masculine, nominative')

    def testCode401(self):
        self.assertEqual(code2term(401), 'possessive pronoun, masculine, genitive')

    def testCode402(self):
        self.assertEqual(code2term(402), 'possessive pronoun, masculine, dative')

    def testCode407(self):
        self.assertEqual(code2term(407), 'possessive pronoun, feminine, nominative')

    def testCode408(self):
        self.assertEqual(code2term(408), 'possessive pronoun, feminine, genitive')

    def testCode409(self):
        self.assertEqual(code2term(409), 'possessive pronoun, feminine, dative')

    def testCode410(self):
        self.assertEqual(code2term(410), 'possessive pronoun, feminine, accusative')

    def testCode411(self):
        self.assertEqual(code2term(411), 'possessive pronoun, feminine, instrumental')

    def testCode412DoesNotExist(self):
        self.assertIsNone(code2term(412))

    def testCode413(self):
        self.assertEqual(code2term(413), 'possessive pronoun, feminine, prepositional')

    def testCode414(self):
        self.assertEqual(code2term(414), 'possessive pronoun, neuter, nominative')

    def testCode415(self):
        self.assertEqual(code2term(415), 'possessive pronoun, neuter, genitive')

    def testCode416(self):
        self.assertEqual(code2term(416), 'possessive pronoun, neuter, dative')

    def testCode417(self):
        self.assertEqual(code2term(417), 'possessive pronoun, neuter, accusative')

    def testCode418(self):
        self.assertEqual(code2term(418), 'possessive pronoun, neuter, instrumental')

    def testCode419(self):
        self.assertEqual(code2term(419), 'possessive pronoun, neuter, prepositional')

    def testCode420(self):
        self.assertEqual(code2term(420), 'possessive pronoun, plural, nominative')

    def testCode421(self):
        self.assertEqual(code2term(421), 'possessive pronoun, plural, genitive')

    def testCode422(self):
        self.assertEqual(code2term(422), 'possessive pronoun, plural, dative')

    def testCode423(self):
        self.assertEqual(code2term(423), 'possessive pronoun, plural, accusative, animate')

    def testCode424(self):
        self.assertEqual(code2term(424), 'possessive pronoun, plural, accusative, inanimate')

    def testCode425(self):
        self.assertEqual(code2term(425), 'possessive pronoun, plural, instrumental')

    def testCode426(self):
        self.assertEqual(code2term(426), 'possessive pronoun, plural, prepositional')

    def testCode200(self):
        self.assertEqual(code2term(200), 'adjective, masculine, nominative')

    def testCode201(self):
        self.assertEqual(code2term(201), 'adjective, masculine, genitive')

    def testCode203(self):
        self.assertEqual(code2term(203), 'adjective, masculine, accusative, animate')

    def testCode204(self):
        self.assertEqual(code2term(204), 'adjective, masculine, accusative, inanimate')

    def testCode205(self):
        self.assertEqual(code2term(205), 'adjective, masculine, instrumental')

    def testCode206(self):
        self.assertEqual(code2term(206), 'adjective, masculine, prepositional')

    def testCode207(self):
        self.assertEqual(code2term(207), 'adjective, feminine, nominative')

    def testCode208(self):
        self.assertEqual(code2term(208), 'adjective, feminine, genitive')

    def testCode209(self):
        self.assertEqual(code2term(209), 'adjective, feminine, dative')

    def testCode210(self):
        self.assertEqual(code2term(210), 'adjective, feminine, accusative')

    def testCode211(self):
        self.assertEqual(code2term(211), 'adjective, feminine, instrumental')

    def testCode213(self):
        self.assertEqual(code2term(213), 'adjective, feminine, prepositional')


class TestCodeToTermAdjectiveNeuter(unittest.TestCase):
    def testCode214(self):
        self.assertEqual(code2term(214), 'adjective, neuter, nominative')

    def testCode215(self):
        self.assertEqual(code2term(215), 'adjective, neuter, genitive')

    def testCode216(self):
        self.assertEqual(code2term(216), 'adjective, neuter, dative')

    def testCode217(self):
        self.assertEqual(code2term(217), 'adjective, neuter, accusative')

    def testCode218(self):
        self.assertEqual(code2term(218), 'adjective, neuter, instrumental')

    def testCode219(self):
        self.assertEqual(code2term(219), 'adjective, neuter, prepositional')


class TestCodeToTermAdjectivePlural(unittest.TestCase):
    def testCode220(self):
        self.assertEqual(code2term(220), 'adjective, plural, nominative')

    def testCode221(self):
        self.assertEqual(code2term(221), 'adjective, plural, genitive')

    def testCode222(self):
        self.assertEqual(code2term(222), 'adjective, plural, dative')

    def testCode223(self):
        self.assertEqual(code2term(223), 'adjective, plural, accusative, animate')

    def testCode224(self):
        self.assertEqual(code2term(224), 'adjective, plural, accusative, inanimate')

    def testCode225(self):
        self.assertEqual(code2term(225), 'adjective, plural, instrumental')

    def testCode226(self):
        self.assertEqual(code2term(226), 'adjective, plural, prepositional')


class TestCodeToTermNoun(unittest.TestCase):
    def testCode1(self):
        self.assertEqual('noun, nominative singular', code2term(1))

    def testCode2(self):
        self.assertEqual('noun, nominative plural', code2term(2))

    def testCode3(self):
        self.assertEqual('noun, genitive singular', code2term(3))

    def testCode4(self):
        self.assertEqual('noun, genitive plural', code2term(4))

    def testCode5(self):
        self.assertEqual('noun, accusative singular', code2term(5))

    def testCode6(self):
        self.assertEqual('noun, accusative plural', code2term(6))

    def testCode7(self):
        self.assertEqual('noun, dative singular', code2term(7))

    def testCode8(self):
        self.assertEqual('noun, dative plural', code2term(8))

    def testCode9(self):
        self.assertEqual('noun, instrumental singular', code2term(9))

    def testCode11(self):
        self.assertEqual('noun, instrumental plural', code2term(11))

    def testCode12(self):
        self.assertEqual('noun, prepositional singular', code2term(12))

    def testCode14(self):
        self.assertEqual('noun, prepositional plural', code2term(14))

    def testCode15(self):
        self.assertEqual('noun, vocative', code2term(15))

    def testCode16(self):
        self.assertEqual('noun, partitive', code2term(16))

    def testCode17(self):
        self.assertEqual('noun, locative', code2term(17))


class TestCodeToTermVerb(unittest.TestCase):
    def testCode300(self):
        self.assertEqual('verb, imperative singular', code2term(300))

    def testCode301(self):
        self.assertEqual('verb, imperative plural', code2term(301))

    def testCode306(self):
        self.assertEqual('verb, present first person singular', code2term(306))

    def testCode307(self):
        self.assertEqual('verb, present second person singular', code2term(307))

    def testCode308(self):
        self.assertEqual('verb, present third person singular', code2term(308))

    def testCode309(self):
        self.assertEqual('verb, present first person plural', code2term(309))

    def testCode310(self):
        self.assertEqual('verb, present second person plural', code2term(310))

    def testCode311(self):
        self.assertEqual('verb, present third person plural', code2term(311))

    def testCode312(self):
        self.assertEqual('verb, future first person singular', code2term(312))

    def testCode313(self):
        self.assertEqual('verb, future second person singular', code2term(313))

    def testCode314(self):
        self.assertEqual('verb, future third person singular', code2term(314))

    def testCode315(self):
        self.assertEqual('verb, future first person plural', code2term(315))

    def testCode316(self):
        self.assertEqual('verb, future second person plural', code2term(316))

    def testCode317(self):
        self.assertEqual('verb, future third person plural', code2term(317))

    def testCode318(self):
        self.assertEqual('verb, present active participle', code2term(318))

    def testCode319(self):
        self.assertEqual('verb, past active participle', code2term(319))

    def testCode320(self):
        self.assertEqual('verb, present adverbial participle', code2term(320))

    def testCode321(self):
        self.assertEqual('verb, past adverbial participle', code2term(321))

    def testCode322(self):
        self.assertEqual('verb, present passive participle', code2term(322))

    def testCode323(self):
        self.assertEqual('verb, past passive participle', code2term(323))


class TestCode2TermPronoun(unittest.TestCase):
    def checkCode(self, term: str, code: int):
        self.assertEqual(term, code2term(code))

    def testCode801(self):
        self.checkCode('pronoun, nominative', 801)

    def testCode802(self):
        self.checkCode('pronoun, genitive', 802)

    def testCode803(self):
        self.checkCode('pronoun, dative', 803)

    def testCode804(self):
        self.checkCode('pronoun, accusative', 804)

    def testCode805(self):
        self.checkCode('pronoun, instrumental', 805)

    def testCode806(self):
        self.checkCode('pronoun, prepositional', 806)

