from enum import Enum, auto
from typing import Optional, Union, List
import re
from functools import lru_cache
import yaml


def rupos2upos(rupos: str) -> Optional[str]:
    """Returns the UPOS tag for a Russian part of speech name

        Parameters
        ----------
        rupos : str
            The Russian part of speech

        Returns
        -------
        str
           The UPOS tag that corresponds to the Russian part of speech, or None
           if no match is found.
        """
    ru = ['существительное', 'прилагательное', 'наречие', 'глагол', 'междометие',
          'имя собственное', 'предлог', 'союз', 'местоимение', 'частица', 'союз', 'числительное']
    upos = ['NOUN', 'ADJ', 'ADV', 'VERB', 'INTJ', 'PROPN', 'ADP', 'CCONJ', 'PRON', 'PART', 'SCONJ']
    try:
        return upos[ru.index(rupos)]
    except ValueError:
        return None


def code2term(code: int) -> str:
    """
    Returns an English-language description for given inflection code
    :param code: The inflection code (as listed in inflection_codes.yaml) to convert
    :return: An English description of the part of speech + inflection information.
    """
    desc = None

    def append_case_min_has_animate(prefix: str, value: int, lowest: int, hasanimate: bool):
        value = value - 1 if value == 213 else value
        value = value - lowest
        cases_anim = {
            0: lambda: 'nominative',
            1: lambda: 'genitive',
            2: lambda: 'dative',
            3: lambda: 'accusative, animate',
            4: lambda: 'accusative, inanimate',
            5: lambda: 'instrumental',
            6: lambda: 'prepositional'
        }
        cases_inanim = {
            0: lambda: 'nominative',
            1: lambda: 'genitive',
            2: lambda: 'dative',
            3: lambda: 'accusative',
            4: lambda: 'instrumental',
            5: lambda: 'prepositional'
        }
        cases = cases_anim if hasanimate else cases_inanim
        case = cases.get(value, lambda: None)()
        if case:
            return f'{prefix}, {case}'
        else:
            return None

    if code == 800:
        return "pronoun"
    elif code == 700:
        return "numeral"
    elif code == 600:
        return "preposition"
    elif code == 500:
        return "adverb"
    elif 400 <= code < 500:
        desc = "possessive pronoun"
        if code <= 406:
            desc = f'{desc}, masculine'

            def append_case(value):
                cases = {
                    400: lambda: 'nominative',
                    401: lambda: 'genitive',
                    402: lambda: 'dative',
                    403: lambda: 'accusative, animate',
                    404: lambda: 'accusative, inanimate',
                }
                return cases[value]()
            desc = f'{desc}, {append_case(code)}'
        elif code <= 413:
            desc = f'{desc}, feminine'

            def append_case(value, prefix: str):
                cases = {
                    407: lambda: 'nominative',
                    408: lambda: 'genitive',
                    409: lambda: 'dative',
                    410: lambda: 'accusative',
                    411: lambda: 'instrumental',
                    413: lambda: 'prepositional'
                }
                case = cases.get(value, lambda: None)()
                if case:
                    return f'{prefix}, {case}'
                else:
                    return None
            desc = append_case(code, desc)
        elif code <= 419:
            desc = f'{desc}, neuter'

            def append_case(value, prefix: str):
                cases = {
                    414: lambda: 'nominative',
                    415: lambda: 'genitive',
                    416: lambda: 'dative',
                    417: lambda: 'accusative',
                    418: lambda: 'instrumental',
                    419: lambda: 'prepositional'
                }
                case = cases.get(value, lambda: None)()
                if case:
                    return f'{prefix}, {case}'
                else:
                    return None
            desc = append_case(code, desc)
        elif code <= 426:
            desc = f'{desc}, plural'

            def append_case(value, _prefix: str):
                cases = {
                    420: lambda: 'nominative',
                    421: lambda: 'genitive',
                    422: lambda: 'dative',
                    423: lambda: 'accusative, animate',
                    424: lambda: 'accusative, inanimate',
                    425: lambda: 'instrumental',
                    426: lambda: 'prepositional'
                }
                case = cases.get(value, lambda: None)()
                if case:
                    return f'{_prefix}, {case}'
                else:
                    return None

            desc = append_case(code, desc)
    elif 200 <= code < 300:
        prefix = 'adjective'

        if 200 <= code <= 206:
            desc = f'{prefix}, masculine'
            desc = append_case_min_has_animate(desc, code, 200, True)
        elif 207 <= code <= 213:
            desc = f'{prefix}, feminine'
            desc = append_case_min_has_animate(desc, code, 207, False)
        elif 214 <= code <= 219:
            desc = f'{prefix}, neuter'
            desc = append_case_min_has_animate(desc, code, 214, False)
        elif 220 <= code <= 226:
            desc = f'{prefix}, plural'
            desc = append_case_min_has_animate(desc, code, 220, True)
    elif 0 <= code < 100:
        prefix = 'noun'

        def append_case_postfix(code_, pre):
            cases = {
                1: lambda: 'nominative singular',
                2: lambda: 'nominative plural',
                3: lambda: 'genitive singular',
                4: lambda: 'genitive plural',
                5: lambda: 'accusative singular',
                6: lambda: 'accusative plural',
                7: lambda: 'dative singular',
                8: lambda: 'dative plural',
                9: lambda: 'instrumental singular',
                11: lambda: 'instrumental plural',
                12: lambda: 'prepositional singular',
                14: lambda: 'prepositional plural',
                15: lambda: 'vocative',
                16: lambda: 'partitive',
                17: lambda: 'locative'
            }
            case = cases.get(code_, lambda: None)()
            if case:
                return f'{pre}, {case}'
            else:
                return None
        desc = append_case_postfix(code, prefix)
    elif 300 <= code < 400:
        prefix = 'verb'

        def append_verb_pos(code_, pre):
            post = {
                300: lambda: 'imperative singular',
                301: lambda: 'imperative plural',
                302: lambda: 'past masculine',
                303: lambda: 'past feminine',
                304: lambda: 'past neuter',
                305: lambda: 'past plural',
                306: lambda: 'present first person singular',
                307: lambda: 'present second person singular',
                308: lambda: 'present third person singular',
                309: lambda: 'present first person plural',
                310: lambda: 'present second person plural',
                311: lambda: 'present third person plural',
                312: lambda: 'future first person singular',
                313: lambda: 'future second person singular',
                314: lambda: 'future third person singular',
                315: lambda: 'future first person plural',
                316: lambda: 'future second person plural',
                317: lambda: 'future third person plural',
                318: lambda: 'present active participle',
                319: lambda: 'past active participle',
                320: lambda: 'present adverbial participle',
                321: lambda: 'past adverbial participle',
                322: lambda: 'present passive participle',
                323: lambda: 'past passive participle',

            }
            p = post.get(code_, lambda: None)()
            if p:
                return f'{prefix}, {p}'
            else:
                return None
        desc = append_verb_pos(code, prefix)
    elif 801 <= code < 900:
        prefix = "pronoun"

        desc = append_case_min_has_animate('pronoun', code, 801, False)

    return desc


class SpeechPart(Enum):
    """
    Part of speech enumeration
    """
    NOUN = auto()
    ADJECTIVE = auto()
    VERB = auto()
    ADVERB = auto()
    PRONOUN_POSSESSIVE = auto()
    PREPOSITION = auto()
    NUMERAL = auto()
    PRONOUN = auto()

    def to_upos(self):
        """
        Converts SpeechPart enumeration to universal POS (UPOS)
        :return: UPOS string for this SpeechPart
        """
        upos_list = ['NOUN', 'ADJ', 'VERB', 'ADV', 'PRON', 'ADP', 'NUM', 'PRON']
        try:
            return upos_list[self.value - 1]
        except IndexError:
            return None


class NounCaseType(Enum):
    """
    Enumeration for noun cases
    """
    NOMINATIVE = auto()
    GENITIVE = auto()
    DATIVE = auto()
    ACCUSATIVE = auto()
    INSTRUMENTAL = auto()
    PREPOSITIONAL = auto()
    LOCATIVE = auto()
    VOCATIVE = auto()

    def case_name_for_type(self):
        """
        Return the name for a given type
        :return: Lower case name of the given type
        """
        return self.name.lower()


class NounInflection(object):
    """
    A NounInflection is a single case with singular and plural forms
    """
    def __init__(self):
        self.singular = []
        self.plural = []

    def add_form(self, issingular: bool, words: List[str]):
        """
        Adds an inflection form
        :param issingular: Set to True if this is a singular form, otherwise plural
        :param words: List of words for this inflection
        :return: Nothing
        """
        for word in words:
            if issingular:
                self.singular.append(word)
            else:
                self.plural.append(word)


class NounCase(object):
    """
    A single noun case, comprising a NounCaseType and an Inflection
    """
    def __init__(self, case_type: NounCaseType, inflection: NounInflection):
        """
        Returns a new instance of the class
        :param case_type: The case type of this noun case
        :param inflection: The inflection information for this case (singular and plural forms)
        """
        self.casetype: NounCaseType = case_type
        self.inflection: NounInflection = inflection


class AdjectiveInflection(object):
    """
    Inflected form of adjective
    """
    def __init__(self):
        self.masculine = None
        self.feminine = None
        self.neuter = None
        self.plural = None

    @classmethod
    def from_term_list(cls, terms: List[str]):
        """
        Returns a new instance of the class from list of inflected forms
        :param terms: A list of forms for a single case. This list is in the order: M, F, N, plural.
        :return: New instance of the class
        """
        obj = cls.__new__(cls)
        super(AdjectiveInflection).__init__()
        obj.masculine = terms[0]
        obj.feminine = terms[2]
        obj.neuter = terms[1]
        obj.plural = terms[3]
        return obj


class AdjectiveCaseType(Enum):
    """
    Adjective case type enumeration
    """
    NOMINATIVE = auto()
    GENITIVE = auto()
    DATIVE = auto()
    ACCUSATIVE = auto()


class Word(object):
    """
    A single word comprising its dictionary form and part of speech
    """
    def __init__(self, word: str, pos: SpeechPart):
        """
        Returns a new instance of Word class
        :param word: The dictionary form of the word
        :param pos: The part of speech as SpeechPart type
        """
        self.value = word
        self.pos = pos


class Pronoun(Word):
    def __init__(self, word):
        super().__init__(word, SpeechPart.PRONOUN)
        self.nominative: Optional[str]
        self.genitive: Optional[str]
        self.dative: Optional[str]
        self.accusative: Optional[str]
        self.instrumental: Optional[str]
        self.prepositional: Optional[str]

    def add_form(self, case_type: NounCaseType, word):
        # ignore cases that pronouns do not have
        if case_type in (NounCaseType.VOCATIVE, NounCaseType.LOCATIVE):
            return
        property_name = NounCaseType.case_name_for_type(case_type)
        setattr(self, property_name, word)

    @property
    @lru_cache()
    def inflection_code_list(self):
        with open('inflection_codes.yaml') as file:
            inflection_codes = yaml.safe_load(file)
        cases = ['nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'prepositional']
        export_words = []
        for casestr in cases:
            code = inflection_codes['pron'][casestr]
            export_words.append((getattr(self, casestr), code))
        return export_words


class Noun(Word):
    """
    A single noun word and all of its inflected forms
    """
    def __init__(self, word: str):
        """
        Returns a new instance of Noun class
        :param word: The dictionary form of the word
        """
        super(Noun, self).__init__(word, SpeechPart.NOUN)
        self.nominative: Optional[NounInflection] = NounInflection()
        self.genitive: Optional[NounInflection] = NounInflection()
        self.dative: Optional[NounInflection] = NounInflection()
        self.accusative: Optional[NounInflection] = NounInflection()
        self.instrumental: Optional[NounInflection] = NounInflection()
        self.prepositional: Optional[NounInflection] = NounInflection()
        self.vocative: Optional[NounInflection] = NounInflection()
        self.locative: Optional[NounInflection] = NounInflection()

    def add_form(self, case_type: NounCaseType, issingular: bool, words: [str]):
        """
        Adds a new form to this noun
        :param case_type: The NounCaseType for this form
        :param issingular: True if singular, otherwise False
        :param words: List of words as strings to add
        :return: Nothing
        """
        property_name = NounCaseType.case_name_for_type(case_type)
        case_inflection: NounInflection = getattr(self, property_name)
        case_inflection.add_form(issingular, words)
        setattr(self, property_name, case_inflection)

    def add_form_case_name(self, casestr: str, issingular: bool, words: [str]):
        if type(words) is not list:
            raise ValueError
        case_inflection: NounInflection = getattr(self, casestr)
        case_inflection.add_form(issingular, words)
        setattr(self, casestr, case_inflection)

    @property
    @lru_cache()
    def inflection_code_list(self):
        """
        Returns a list of parsed words and inflection codes as defined in inflection_codes.yaml
        :return: Returns a list of tuples whose first member is the inflected form of
        the noun and whose second member is the inflection code.
        """
        with open('inflection_codes.yaml') as file:
            inflection_codes = yaml.safe_load(file)
        cases = ['nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'prepositional',
                 'locative', 'vocative']
        export_words = []
        for casestr in cases:
            case_inflection: NounInflection = getattr(self, casestr)
            if case_inflection:
                singulars = case_inflection.singular
                for w in singulars:
                    code = inflection_codes['noun']['singular'][casestr]
                    export_words.append((w, code))
                plurals = case_inflection.plural
                for w in plurals:
                    code = inflection_codes['noun']['plural'][casestr]
                    export_words.append((w, code))
        return export_words


class AdjectiveLike(Word):
    """
    Base class for an adjective-like object
    """
    def __init__(self, word: str, pos: SpeechPart):
        """
        Returns a newly initialized instance of the Adjective class
        :param word: the uninflected form of the adjective
        :param pos: the part of speeech of the type requested
        """
        super(AdjectiveLike, self).__init__(word, SpeechPart.ADJECTIVE)
        self.nominative: Optional[AdjectiveInflection] = AdjectiveInflection()
        self.genitive: Optional[AdjectiveInflection] = AdjectiveInflection()
        self.dative: Optional[AdjectiveInflection] = AdjectiveInflection()
        self.accusative_animate: Optional[AdjectiveInflection] = AdjectiveInflection()
        self.accusative_inanimate: Optional[AdjectiveInflection] = AdjectiveInflection()
        self.instrumental: Optional[AdjectiveInflection] = AdjectiveInflection()
        self.prepositional: Optional[AdjectiveInflection] = AdjectiveInflection()
        self.short_form: Optional[AdjectiveInflection] = AdjectiveInflection()
        if SpeechPart == SpeechPart.ADJECTIVE:
            self._code_prefix = 'adj'
        elif SpeechPart == SpeechPart.PRONOUN_POSSESSIVE:
            self._code_prefix = 'pronoun_possessive'

    def code_prefix(self):
        return self._code_prefix

    @property
    @lru_cache()
    def inflection_code_list(self):
        """
        Returns all of the inflected forms of the adjective as list of tuples :return: Inflected forms and their
        codes as list of tuples, the first member of which is the word and the second is the inflection code.
        """
        with open('inflection_codes.yaml') as file:
            inflection_codes = yaml.safe_load(file)
        cases = ['nominative', 'genitive', 'dative', 'accusative_animate',
                 'accusative_inanimate', 'instrumental', 'prepositional',
                 'short_form']
        export_words = []
        for casestr in cases:
            caseinflection: AdjectiveInflection = getattr(self, casestr)
            masc_form = caseinflection.masculine
            m = re.search(r'accusative_(.*)$', casestr, re.M)
            if m:
                animacy = m[1]
                export_words.append((masc_form, inflection_codes[self.code_prefix()]['masculine']['accusative'][animacy]))
            normalized_casestr = 'accusative' if casestr.startswith('accusative') else casestr
            if normalized_casestr == 'short_form':
                try:
                    export_words.append((caseinflection.feminine, inflection_codes[self.code_prefix()]['short']['feminine']))
                    export_words.append((caseinflection.masculine, inflection_codes[self.code_prefix()]['short']['masculine']))
                    export_words.append((caseinflection.neuter, inflection_codes[self.code_prefix()]['short']['neuter']))
                    export_words.append((caseinflection.plural, inflection_codes[self.code_prefix()]['short']['plural']))
                except KeyError:
                    pass
            else:
                # feminine forms have alternatve instrumental singular forms
                # so attempt to split
                fem_forms = caseinflection.feminine
                for fem_form in fem_forms.split():
                    if fem_form != '-':
                        try:
                            export_words.append((fem_form, inflection_codes[self.code_prefix()]['feminine'][normalized_casestr]))
                        except KeyError:
                            print(f"*** ERROR → code_prefix = {self.code_prefix()}, casestr = {normalized_casestr}")
                plural_form = caseinflection.plural
                if plural_form != '-':
                    if m:
                        animacy = m[1]
                        export_words.append((plural_form, inflection_codes[self.code_prefix()]['plural'][normalized_casestr][animacy]))
                    else:
                        export_words.append((plural_form, inflection_codes[self.code_prefix()]['plural'][normalized_casestr]))
                neuter_form = caseinflection.neuter
                if neuter_form != '-':
                    export_words.append((neuter_form, inflection_codes[self.code_prefix()]['neuter'][normalized_casestr]))
        return export_words

        # todo
        # how to deal with comparative and superlative degrees?


class Adjective(AdjectiveLike):
    """
    An Adjective object
    """
    def __init__(self, word: str):
        super(Adjective, self).__init__(word, SpeechPart.ADVERB)

    def code_prefix(self):
        """
        Returns the object's code prefix for inflection code discovery
        :return: Returns the object's code prefix
        """
        return 'adj'


class PossessivePronoun(AdjectiveLike):
    """
    A possessive pronoun object
    """
    def __init__(self, word: str):
        super(PossessivePronoun, self).__init__(word, SpeechPart.PRONOUN_POSSESSIVE)

    def code_prefix(self):
        """
        Returns the object's code prefix for inflection code discovery
        :return: Returns the object's code prefix
        """
        return 'pronoun_possessive'


class VerbTensePlurality(object):
    """
    An object that encapsulates three persons (1st person, 2nd person, 3rd person) within a verb conjugation.
    """
    def __init__(self):
        self.p1 = None
        self.p2 = None
        self.p3 = None


class VerbTense(object):
    """
    A verb tense, encapsulating singular and plural columns
    """
    def __init__(self):
        self.singular = VerbTensePlurality()
        self.plural = VerbTensePlurality()

    def add_form_issingular(self, issingular: bool, form: str, person: int):
        """
        Adds a form to the verb tense object
        :param issingular: True if singular, otherwise False
        :param form: The conjugated Russian verb form to add
        :param person: Integer representing person (1 for first-person, etc.)
        :return: Nothing
        """
        if not 1 <= person <= 3:
            return
        accessor = f'p{person}'
        if issingular:
            setattr(self.singular, accessor, form)
        else:
            setattr(self.plural, accessor, form)

    def add_form_list(self, forms):
        """
        Adds a list of six forms to a verb tense/
        :param forms: List of six forms to add in order (1st person singular, 2nd person singular...3rd person plural)
        :return: Mothing
        """
        for idx, form in enumerate(forms):
            number = 1 if idx < 3 else 2
            person = idx % 3 + 1
            issingular: bool = (number == 1)
            self.add_form_issingular(issingular,form, person)

    def getform_for_numberstr_personstr(self, num: str, person: str):
        """
        Returns a conjugated verb form within this tense given number and person.
        :param num: The number, 'singular' for singular, 'plural' for plural as string.
        :param person: The person, 'p1' for first-person, 'p2' for second-person, 'p3' for third-person.
        :return: The form for the described parameters.
        """
        plurality = getattr(self, num)
        form = getattr(plurality, person)
        return form


class VerbPastTense(object):
    """
    A verb past tense

    Attributes:
        masculine    The masculine form of the past tense
        feminine    The feminine form of the past tense
        neuter      The neuter form of the past tense
        plural      The plural form of the past tense
    """
    def __init__(self):
        self.masculine = None
        self.feminine = None
        self.neuter = None
        self.plural = None


class VerbImperativeTense(object):
    """
    A verb imperative tense

    Attributes:
        singular    The singular form.
        plural      The plural form.
    """
    def __init__(self):
        self.singular = None
        self.plural = None


class Verb(Word):
    """
    A Russian verb object

    Attributes:
        present                         The present tense VerbTense object
        future                          The future tense VerbTense object
        past                            The past tense VerbPastTense object
        imperative                      The imperative tense VerbImperativeTense object
        present_active_participle       Present active participle
        past_active_participle          Past active participle
        present_adverbial_participle    Present adverbial participle
        past_adverbial_participle       Past adverbial participle
        present_passive_participle      Present passive participle
        past_passive_participle         Past passive participle
    """
    def __init__(self, word:str):
        super(Verb, self).__init__(word, SpeechPart.VERB)
        self.present = VerbTense()
        self.future = VerbTense()
        self.past = VerbPastTense()
        self.imperative = VerbImperativeTense()
        self.present_active_participle = None
        self.past_active_participle = None
        self.present_adverbial_participle = None
        self.past_adverbial_participle = []
        self.present_passive_participle = None
        self.past_passive_participle = None

    def add_past_form(self, word: str, genderstr: str):
        """
        Add a single past tense form.
        :param word: The verb form to add, for example, делал
        :param genderstr: The gender as string, one of 'masculine', 'feminine', 'neuter', or 'plural'
        :return: Nothing
        """
        if genderstr not in ['masculine', 'feminine', 'neuter', 'plural']:
            return
        setattr(self.past, genderstr, word)

    def has_present_tense(self):
        """
        Returns whether object has a present tense or not.
        :return: Returns a bool True if there is a present tense, otherwise False
        """
        return self.present.singular.p1 is not None

    def has_future_tense(self):
        """
        Returns whether object has a future tense or not.
        :return: Returns a bool True if there is a future tense, otherwise False
        """
        return self.future.singular.p1 is not None

    def has_tense_named(self, name: str) -> bool:
        """
        Returns whether the object has named tense or note.
        :param name: The tense name as str, one of 'present', 'future', 'past', 'imperative'.
        :return: True if the object has the named tense, otherwise False.
        """
        if len(name.split(' ')) == 1:
            if name == 'present':
                return self.has_present_tense()
            elif name == 'future':
                return self.has_future_tense()
            elif name == 'past':
                return self.past.masculine is not None
            elif name == 'imperative':
                return self.imperative.singular is not None

    @staticmethod
    def matching_list_item(src: [str], dst: [str], item: str):
        try:
            return dst[src.index(item)]
        except ValueError:
            return None

    @property
    @lru_cache()
    def inflection_code_list(self):
        """
        Returns a list of inflection codes for the valid forms of this verb :return: Inflection codes for this verb a
        list of tuples, the first member of which is the form and the second is the inflection code.
        """
        with open('inflection_codes.yaml') as file:
            inflection_codes = yaml.safe_load(file)
        export_words = []
        src_list = ['p1', 'p2', 'p3']
        p_list = ['first_person', 'second_person', 'third_person']
        tenses = ['present', 'future']
        pluralities = ['singular', 'plural']
        genders = ['masculine', 'feminine', 'neuter', 'plural']
        if self.has_present_tense():
            for number in pluralities:
                for person in src_list:
                    p = self.matching_list_item(src_list, p_list, person)
                    code = inflection_codes['verb']['present'][number][p]
                    form = self.present.getform_for_numberstr_personstr(number, person)
                    export_words.append((form, code))
        if self.has_future_tense():
            for number in pluralities:
                for person in src_list:
                    p = self.matching_list_item(src_list, p_list, person)
                    code = inflection_codes['verb']['future'][number][p]
                    form = self.future.getform_for_numberstr_personstr(number, person)
                    export_words.append((form, code))
        if self.has_tense_named('past'):
            for gender in genders:
                code = inflection_codes['verb']['past'][gender]
                form = getattr(self.past, gender)
                export_words.append((form, code))
        if self.has_tense_named('imperative'):
            for number in pluralities:
                code = inflection_codes['verb']['imperative'][number]
                form = getattr(self.imperative, number)
                export_words.append((form, code))
        if self.present_active_participle:
            code = inflection_codes['verb']['participle']['active']['present']
            export_words.append((self.present_active_participle, code))
        if self.past_active_participle:
            code = inflection_codes['verb']['participle']['active']['past']
            export_words.append((self.past_active_participle, code))
        if self.past_passive_participle:
            code = inflection_codes['verb']['participle']['passive']['past']
            export_words.append((self.past_passive_participle, code))
        if self.present_passive_participle:
            code = inflection_codes['verb']['participle']['passive']['present']
            export_words.append((self.present_passive_participle, code))
        if self.present_adverbial_participle:
            code = inflection_codes['verb']['participle']['adverbial']['present']
            export_words.append((self.present_adverbial_participle, code))
        if len(self.past_adverbial_participle) > 0:
            for variant in self.past_adverbial_participle:
                code = inflection_codes['verb']['participle']['adverbial']['past']
                export_words.append((variant, code))
        return export_words
