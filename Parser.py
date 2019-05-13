import json, re

from phonology.phonology import vowel, fricative2plosive, Phonology, Pattern

class Parser():

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def __init__(self):
        with open("lexicon/conjugation.json","r") as v:
            self.verb_endings = json.load(v)
        with open("lexicon/declension.json","r") as n:
            self.noun_endings = json.load(n)
        with open("lexicon/patterns.json", "r") as p:
            self.patterns = json.load(p)
        self.phonology = Phonology(inventory_path='./phonology/inventory',rules_path='./phonology/rules')

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def parse_verb(self, verb):

        # get possible verbs sorted in order of shortest suffix-less form
        affix_options = sorted(self.match_morphemes(dict=self.verb_endings, string=verb, morpheme_type="affix"), key=lambda x:len(x[2]))
        inflection_possibilities = []

        for (affix, word, stem, parse) in affix_options[:1]:
            #print(affix, word, stem, parse)
            #skeleton = Pattern(pattern='',inventory=self.phonology.inventory).make_skeleton(stem)#self.get_skeleton(stem)
            #print(skeleton)
            patterns = self.match_morphemes(dict=self.patterns, string=stem, morpheme_type="skeleton")
            #print(patterns)
            if len(patterns) > 0:
                for p in patterns:
                    inflection_possibilities.append("_".join([p[-1], parse]))

        return inflection_possibilities

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def parse_noun(self, noun):
        pass

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def match_morpheme(self, morpheme, string, morpheme_type='affix'):
        '''
        :param affix: prefix, suffix or circumfix
        :param string:
        :return: determines if string has this affix
        '''
        if morpheme_type == 'affix':
            return(bool(re.fullmatch(pattern=morpheme, string=string)))
        elif morpheme_type == 'skeleton':
            #print("HERE")
            #print("morpheme", morpheme)
            #print("string", string)
            return Pattern(pattern=morpheme, inventory=self.phonology.inventory).match(string)

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def remove_affix(self, affix, string):
        '''
        :param affix:
        :param string:
        :return: returns string with affix removed from it
        '''
        return re.sub(pattern=affix, string=string, repl='\g<1>')

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def match_morphemes(self, dict, string, path=[], morpheme_type="affix"):
        '''
        :param dict: [nested] dictionary of paradigms
        :param string: word to match
        :param path: to store grammatical values recursively
        :param type: "affixes" or "skeleton", depending on whether matching affixes or the skeleton itself
        :return: list of possibilities of form [(affix, string_original, string_stripped_of_affix, grammatical_value)]
        '''

        if (type(dict) == str):
            value = []
            morpheme = dict
            if self.match_morpheme(morpheme=morpheme, string=string, morpheme_type=morpheme_type):
                if morpheme_type == "affix":
                    value.append((morpheme, string, self.remove_affix(morpheme, string), "_".join(path)))
                elif morpheme_type == "skeleton":
                    value.append((morpheme, string, "_".join(path)))
            return(value)

        elif (type(dict) == list):
            values = []
            for morpheme in dict:
                if self.match_morpheme(morpheme=morpheme, string=string, morpheme_type=morpheme_type):
                    if morpheme_type == "affix":
                        value = (morpheme, string, self.remove_affix(morpheme, string), "_".join(path))
                        values.append(value)
                    elif morpheme_type == "skeleton":
                        value = (morpheme, string, "_".join(path))
                        values.append(value)
            return values

        else:
            possibilities = []
            for i, v in enumerate(dict.values()):
                path_prime = path.copy()
                path_prime.append(list(dict.keys())[i])
                possibilities.extend(self.match_morphemes(v, string, path_prime, morpheme_type=morpheme_type))
            return possibilities

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

if __name__ == '__main__':
    P = Parser()
    #print(P.get_skeleton(string))
    #options = P.parse_verb("teḵtvin")
    #options = P.parse_verb("teṯkaṯbun")
    #options = P.parse_verb("neṯkṯev")
    options = P.parse_verb("keṯvaṯ")

    #possibilities = P.match_morphemes(dict=P.verb_endings, string="teḵtvin")
    print(options)