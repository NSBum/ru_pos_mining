import random
import urllib.parse
from urllib.request import urlopen, Request
from lxml import etree
import html
import re
import json
from functools import lru_cache
from grammar import *
import yaml
from enum import Enum, auto
from typing import Optional, Union


def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist


class VerbTenseType(Enum):
    PRESENT = auto()
    FUTURE = auto()


class VerbTableRow(Enum):
    FIRST_PERSON_SINGULAR = 1
    SECOND_PERSON_SINGULAR = 2
    THIRD_PERSON_SINGULAR = 3
    FIRST_PERSON_PLURAL = 4
    SECOND_PERSON_PLURAL = 5
    THIRD_PERSON_PLURAL = 6


class CaseTableRow(Enum):
    HEADER = 0


class AdjectiveTableRow(Enum):
    NOMINATIVE = 2
    GENITIVE = 3
    DATIVE = 4
    ACCUSATIVE_ANIMATE = 5
    ACCUSATIVE_INANIMATE = 6
    INSTRUMENTAL = 7
    PREPOSITIONAL = 8
    SHORT = 9


class CaseCell(Enum):
    CASE = 0
    SINGULAR = 1
    PLURAL = 2


class CaseTranslateDirection(Enum):
    RU2EN = 0
    EN2RU = 1


def cyrillic(text):
    return html.unescape(text)


def casetranslate(casestr: str, direction: CaseTranslateDirection) -> Optional[str]:
    case_names_en = ['nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'prepositional', 'locative',
                     'vocative']
    case_names_ru = ['именительный', 'родительный', 'дательный', 'винительный', 'творительный', 'предложный',
                     'местный падеж', 'звательный падеж']
    (source, dest) = (case_names_en, case_names_ru) if direction == CaseTranslateDirection.EN2RU else (
        case_names_ru, case_names_en)
    try:
        return dest[source.index(casestr)]
    except ValueError:
        return None


def col_idx_to_en_number(col_idx: int) -> Optional[str]:
    return ['singular', 'plural'][col_idx - 1] if 1 <= col_idx <= 2 else None


class RuWikitionary(object):
    def __init__(self, word: str, use_local: bool = False, local_fn=None):
        self.use_local = use_local
        self.word = word
        self.local_fn = local_fn

    @property
    @lru_cache()
    def url(self) -> str:
        """Returns the Russian Wiktionary for object's word

        """
        ru_word = urllib.parse.quote(self.word)
        return f"https://ru.wiktionary.org/wiki/{ru_word}"

    @property
    @lru_cache()
    def url_response(self):
        """
        Using rotating user-agent values in the header returns the response
        object from web request to Russian Wiktionary page

        :return: urlopen Response object
        """
        user_agents = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 '
            'Safari/535.19',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 '
            'Safari/537.36 Edge/12.246',
            'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 '
            'Safari/537.36 '
        ]
        randomint = random.randint(0, 9)
        headers = {'user-agent': user_agents[randomint]}
        try:
            response = urlopen(Request(self.url, headers=headers))
        except urllib.error.HTTPError:
            response = None
        return response

    @property
    @lru_cache()
    def root_tree(self):
        """
        The root tree for the Russian word page.
        :return: The root tree for the page
        """
        htmlparser = etree.HTMLParser()
        if self.use_local:
            tree = etree.parse(f'html_samples/{self.local_fn}', htmlparser)
        else:
            if self.url_response is None:
                return None
            tree = etree.parse(self.url_response, htmlparser)
        # could use scrapy for this
        # but if you read() the url_response, it consumes it
        # then the response is invalid for using in the lxml etree
        # context

        # selector = scrapy.Selector(text=self.url_response.read(), type='html')
        # extract_list = selector.xpath('''//*[@id="mw-content-text"]/div[1]/p[2]//text()''').extract()
        # extract_str = ''.join(extract_list)
        return tree

    def alternate_morphology(self):
        b = self.root_tree.xpath('''//*[@id="mw-content-text"]/div[1]/p[3]//text()''')
        b_str = ' '.join([x.strip() for x in b]).lower()
        return b_str

    @property
    @lru_cache()
    def pos(self):
        """
        Accessor for the part of speech property
        :return:
        """
        if self.root_tree is None:
            return None
        b = self.root_tree.xpath('''//*[@id="mw-content-text"]/div[1]/p[2]//text()''')
        b_str = ' '.join([x.strip() for x in b]).lower()
        # preposition like в, с, к can fail because their morphological information
        # is not in the usual spot
        if b_str.strip() == self.word:
            b_str = self.alternate_morphology()
        return SpeechPart.from_wiki_text(b_str)

    def parse_noun(self) -> Optional[Noun]:
        """
        Parses the page for noun inflection
        :return: A Noun object or None
        """
        noun = Noun(self.word)
        # some words, e.g. кошка have a table for every sense
        # so we'll try to use only the first one for simplicity
        # //*[@id="mw-content-text"]/div[1]/table[2]
        pre_path = '//*[@id="mw-content-text"]/div[1]/table[contains(@class, "morfotable") and contains(@class, "ru")]'
        pre_block = self.root_tree.xpath(pre_path)
        tbody_block = pre_block[0].getchildren()
        block = tbody_block[0].getchildren()

        for idx, case_row in enumerate(block):
            if idx != CaseTableRow.HEADER.value:
                cell_block = case_row.xpath('td')
                case_text = ''
                for cell_idx, cell in enumerate(cell_block):
                    if cell_idx == CaseCell.CASE.value:
                        # the case name is embedded in an attribute 'title'
                        # of <a> tag
                        a_block = cell.xpath('a')
                        case_text = a_block[0].get('title')
                    else:
                        forms = []
                        # some cases have alternate forms which we need to check for
                        # test for these multiples by looking for a <br/> tag in the HTML'
                        ct = cell.itertext()
                        for w_ct in ct:
                            forms.append(w_ct.strip())
                        number = col_idx_to_en_number(cell_idx)
                        encase = casetranslate(case_text, CaseTranslateDirection.RU2EN)
                        for form in forms:
                            issingular = True if cell_idx == 1 else False
                            noun.add_form_case_name(encase, issingular, [form])
        return noun

    def parse_pronoun(self) -> Optional[Pronoun]:
        pronoun = Pronoun(self.word)
        # this is a little fragile but unless the page formatting
        # changes drastically, it should work because just relying on the order
        # of tables on the page is too variable
        table_rules = 'contains(@rules, "all") and contains(@width, "210")'
        table_path = f'//table[{table_rules}]/tbody/tr'
        block = self.root_tree.xpath(table_path)
        for idx, case_row in enumerate(block):
            if idx < 1:
                continue
            else:
                td = case_row.getchildren()[1]
                cases = [NounCaseType.NOMINATIVE, NounCaseType.GENITIVE, NounCaseType.DATIVE,
                         NounCaseType.ACCUSATIVE, NounCaseType.INSTRUMENTAL, NounCaseType.PREPOSITIONAL]
                pronoun.add_form(cases[idx-1], td.text.strip())
        return pronoun

    def parse_adjective(self) -> Optional[Adjective]:
        """
        Parses the page for adjective inflection.
        :return: Either a parse Adjective object or None
        """
        adjective = Adjective(self.word)
        root_path = '//*[@id="mw-content-text"]/div[1]/table[contains(@class, "morfotable") and contains(@class, ' \
                    '"ru")]/tbody/tr'
        block = self.root_tree.xpath(root_path)
        for idx, case_row in enumerate(block):
            if idx < 2:
                continue
            else:
                inner_idx = 0
                casestr = None
                adjforms = ['masculine', 'feminine', 'neuter', 'plural']
                row_words = []
                for cell_idx, cell in enumerate(case_row.xpath('td')):
                    # read the <td>/<a> title
                    if cell_idx == 0:
                        a_block = cell.xpath('a')
                        case_or_animacy_text = a_block[0].get('title')
                    else:
                        try:
                            celltext = cell.text.strip()
                            row_words.append(celltext)
                        except AttributeError:
                            pass
                if idx == AdjectiveTableRow.NOMINATIVE.value:
                    adjective.nominative = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.GENITIVE.value:
                    adjective.genitive = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.DATIVE.value:
                    adjective.dative = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.INSTRUMENTAL.value:
                    adjective.instrumental = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.PREPOSITIONAL.value:
                    adjective.prepositional = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.ACCUSATIVE_ANIMATE.value:
                    # exclude list items that aren't actual words
                    row_words = [w for w in row_words if len(w) > 1]
                    adjective.accusative_animate = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.ACCUSATIVE_INANIMATE.value:
                    row_words[1:1] = [adjective.accusative_animate.neuter, adjective.accusative_animate.feminine]
                    adjective.accusative_inanimate = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.SHORT.value:
                    adjective.short_form = AdjectiveInflection.from_term_list(row_words)
        return adjective

    def parse_verb(self) -> Optional[Verb]:
        """
        Parses the page for verb conjugation information
        :return: A parsed Verb object or None
        """
        verb = Verb(self.word)
        base_tense = None
        # past tense forms found
        (pmf, pff, pnf, ppf) = (False, False, False, False)
        root_path = '//*[@id="mw-content-text"]/div[1]/table[contains(@class, "morfotable") and contains(@class, ' \
                    '"ru")]/tbody/tr '
        block = self.root_tree.xpath(root_path)
        for idx, case_row in enumerate(block):
            if idx == 0:
                for header_col_idx, header_td in enumerate(case_row.xpath('th')):
                    if header_col_idx == 0:
                        continue
                    # the the <td>/<a> title
                    base_tense: Optional[VerbTenseType] = None
                    base_tense_text = header_td.xpath('a')[0].get('title')
                    if base_tense_text == 'настоящее время':
                        base_tense = VerbTenseType.PRESENT
                        break
                    elif base_tense_text == 'будущее время':
                        base_tense = VerbTenseType.FUTURE
                        break
            elif 1 <= idx <= 6:
                # these rows contain the base cases, past tense and imperative forms
                number = 1 if idx < 4 else 2
                person = idx - 3 * (number - 1)
                # iterate the columns of this row
                column_block = case_row.xpath('td')
                for col_idx, column in enumerate(column_block):
                    celltext = None
                    if column.text:
                        celltext = column.text.strip()
                    if col_idx == 1:
                        if number == 1:
                            if base_tense == VerbTenseType.PRESENT:
                                verb.present.add_form_issingular(True, celltext, person)
                            else:
                                verb.future.add_form_issingular(True, celltext, person)
                        else:
                            if base_tense == VerbTenseType.PRESENT:
                                verb.present.add_form_issingular(False, celltext, person)
                            else:
                                verb.future.add_form_issingular(False, celltext, person)
                    elif col_idx == 2:
                        # past tense column
                        celltexts = column.xpath('text()')
                        if celltexts:
                            celltexts = [x.strip() for x in celltexts]
                            for past_text_idx, past_text in enumerate(celltexts):
                                if number == 1 and person == 1:
                                    # the first item is masculine and second is feminine
                                    if past_text_idx == 0:
                                        # masculine
                                        if not pmf:
                                            verb.add_past_form(past_text, 'masculine')
                                            pmf = True
                                    else:
                                        # feminine
                                        if not pff:
                                            verb.add_past_form(past_text, 'feminine')
                                            pff = True
                                elif number == 1 and person == 3:
                                    if past_text_idx == 2:
                                        if not pnf:
                                            verb.add_past_form(past_text, 'neuter')
                                            pnf = True
                                elif number == 2 and person == 1:
                                    if not ppf:
                                        verb.add_past_form(past_text, 'plural')
                    elif col_idx == 3:
                        # imperative column
                        if person == 2:
                            if number == 1:
                                verb.imperative.singular = celltext
                            else:
                                verb.imperative.plural = celltext
            elif idx > 6:
                # now we have to figure out how to assign content
                # because the rows vary
                # enumerate the columns in this row
                column_block = case_row.xpath('td')
                current_pos = None
                for col_idx, column in enumerate(column_block):
                    if col_idx == 0:
                        # first column is always the part of speech information
                        pos_text = column.xpath('a/@title')
                        if len(pos_text) > 1:
                            pos_str = ' '.join(pos_text)
                            pos_text = ' '.join(unique_list(pos_str.split()))
                            current_pos = pos_text
                        else:
                            current_pos = pos_text[0]
                    elif col_idx == 1:
                        # this is the column with actual form(s)
                        # the forms could be multiple so account for that
                        if current_pos == 'будущее время':
                            # deal with future tense, this must be an imperfective verb
                            aux_verbs = ['буду', 'будешь', 'будет',
                                         'будем', 'будете', 'будут']
                            future_verbs = [f'{x} {self.word}' for x in aux_verbs]
                            verb.future.add_form_list(future_verbs)
                        else:
                            forms_list = column.xpath('a/text()')
                            for form in forms_list:
                                if current_pos == 'действительное причастие прошедшего времени':
                                    # this is a past active participle
                                    verb.past_active_participle = form
                                elif current_pos == 'действительное причастие настоящего времени':
                                    # this is a present active participle
                                    verb.present_active_participle = form
                                elif current_pos == 'деепричастие настоящее время':
                                    verb.present_adverbial_participle = form
                                elif current_pos == 'деепричастие прошедшее время':
                                    verb.past_adverbial_participle.append(form)
                                elif current_pos == 'страдательное причастие настоящего времени':
                                    verb.present_passive_participle = form
                                elif current_pos == 'страдательное причастие прошедшего времени':
                                    verb.past_passive_participle = form

        return verb

    def parse_possessive_pronoun(self) -> Optional[PossessivePronoun]:
        """
        Extracts declension information for a possessive pronoun.
        :return: A PossessivePronoun object or None
        """
        pronoun = PossessivePronoun(self.word)
        root_path = '//*[@id="mw-content-text"]/div[1]/table[contains(@class, "morfotable") and contains(@class, ' \
                    '"ru")]/tbody/tr'
        block = self.root_tree.xpath(root_path)
        last_row_words = []
        for idx, case_row in enumerate(block):
            if idx < 2:
                continue
            else:
                inner_idx = 0
                casestr = None
                adjforms = ['masculine', 'feminine', 'neuter', 'plural']
                row_words = []
                for cell_idx, cell in enumerate(case_row.xpath('td')):
                    # read the <td>/<a> title
                    if idx == AdjectiveTableRow.ACCUSATIVE_ANIMATE.value:
                        if cell_idx > 1:
                            row_words.append(cell.text.strip())
                    elif idx == AdjectiveTableRow.ACCUSATIVE_INANIMATE.value:
                        # accusative inanimate is tricky because the neuter and feminine
                        # forms aren't listed in the table
                        if cell_idx == 1:
                            row_words.append(cell.text.strip())
                            # add add the neuter and feminine forms that are missing from table
                            row_words.extend(last_row_words[1:3])
                        elif cell_idx > 1:
                            row_words.append(cell.text.strip())
                    elif idx == AdjectiveTableRow.INSTRUMENTAL.value:
                        if cell_idx > 0:
                            ct = ' '.join(cell.itertext()).strip()
                            row_words.append(ct)
                    else:
                        if cell_idx > 0:
                            row_words.append(cell.text.strip())
                    if cell_idx == 0:
                        a_block = cell.xpath('a')
                        case_or_animacy_text = a_block[0].get('title')
                if idx == AdjectiveTableRow.NOMINATIVE.value:
                    pronoun.nominative = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.GENITIVE.value:
                    pronoun.genitive = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.DATIVE.value:
                    pronoun.dative = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.INSTRUMENTAL.value:
                    pronoun.instrumental = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.PREPOSITIONAL.value:
                    pronoun.prepositional = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.ACCUSATIVE_ANIMATE.value:
                    pronoun.accusative_animate = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.ACCUSATIVE_INANIMATE.value:
                    pronoun.accusative_inanimate = AdjectiveInflection.from_term_list(row_words)
                last_row_words = row_words
        return pronoun

    def parse_demonstrative_pronoun(self) -> Optional[DemonstrativePronoun]:
        """
        Extracts declension information for a demonstrative pronoun.
        :return: A PossessivePronoun object or None
        """
        pronoun = DemonstrativePronoun(self.word)
        root_path = '//*[@id="mw-content-text"]/div[1]/table[contains(@class, "morfotable") and contains(@class, ' \
                    '"ru")]/tbody/tr'
        block = self.root_tree.xpath(root_path)
        last_row_words = []
        for idx, case_row in enumerate(block):
            if idx < 2:
                continue
            else:
                inner_idx = 0
                casestr = None
                adjforms = ['masculine', 'feminine', 'neuter', 'plural']
                row_words = []
                for cell_idx, cell in enumerate(case_row.xpath('td')):
                    # read the <td>/<a> title
                    if idx == AdjectiveTableRow.ACCUSATIVE_ANIMATE.value:
                        if cell_idx > 1:
                            row_words.append(cell.text.strip())
                    elif idx == AdjectiveTableRow.ACCUSATIVE_INANIMATE.value:
                        # accusative inanimate is tricky because the neuter and feminine
                        # forms aren't listed in the table
                        if cell_idx == 1:
                            row_words.append(cell.text.strip())
                            # add add the neuter and feminine forms that are missing from table
                            row_words.extend(last_row_words[1:3])
                        elif cell_idx > 1:
                            row_words.append(cell.text.strip())
                    elif idx == AdjectiveTableRow.INSTRUMENTAL.value:
                        if cell_idx > 0:
                            ct = ' '.join(cell.itertext()).strip()
                            row_words.append(ct)
                    else:
                        if cell_idx > 0:
                            row_words.append(cell.text.strip())
                    if cell_idx == 0:
                        a_block = cell.xpath('a')
                        case_or_animacy_text = a_block[0].get('title')
                if idx == AdjectiveTableRow.NOMINATIVE.value:
                    pronoun.nominative = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.GENITIVE.value:
                    pronoun.genitive = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.DATIVE.value:
                    pronoun.dative = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.INSTRUMENTAL.value:
                    pronoun.instrumental = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.PREPOSITIONAL.value:
                    pronoun.prepositional = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.ACCUSATIVE_ANIMATE.value:
                    pronoun.accusative_animate = AdjectiveInflection.from_term_list(row_words)
                elif idx == AdjectiveTableRow.ACCUSATIVE_INANIMATE.value:
                    pronoun.accusative_inanimate = AdjectiveInflection.from_term_list(row_words)
                last_row_words = row_words
        return pronoun

    def parse(self) -> Union[Verb, Adjective, Noun, PossessivePronoun, None]:
        """
        Parses the page for inflection info, returning the appropriate part of speech object
        :return: Any of Verb, Adjective, Noun, DemonstrativePronoun, or PossessivePronoun objects (or None)
        """
        if self.pos == SpeechPart.NOUN:
            return self.parse_noun()
        elif self.pos == SpeechPart.ADJECTIVE:
            return self.parse_adjective()
        elif self.pos == SpeechPart.VERB:
            return self.parse_verb()
        elif self.pos == SpeechPart.PRONOUN_POSSESSIVE:
            return self.parse_possessive_pronoun()
        elif self.pos == SpeechPart.PRONOUN:
            return self.parse_pronoun()
        elif self.pos == SpeechPart.PRONOUN_DEMONSTRATIVE:
            return self.parse_demonstrative_pronoun()
