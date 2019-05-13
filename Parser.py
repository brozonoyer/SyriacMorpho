import json, re

from phonology.inventory import vowel, fricative2plosive

class Parser():

    def __init__(self):
        with open("lexicon/conjugation.json","r") as v:
            self.verb_endings = json.load(v)
        with open("lexicon/declension.json","r") as n:
            self.noun_endings = json.load(n)
        with open("lexicon/patterns.json", "r") as p:
            self.patterns = json.load(p)

    def get_skeleton(self, string):
        '''
        :param string:
        :return: verbal skeleton of Cs and Vs
        '''
        skeleton = []
        #radicals = []
        num_Cs = 0
        for x in string:
            if x in vowel:
                skeleton.append(x)
            else:
                num_Cs += 1
                skeleton.append(str(num_Cs) + self.determine_consonant(x))
        #        radicals.append(self.get_radical(x))
        return "_".join(skeleton)#, "_".join(radicals)

    def syllabify(self, string):
        pass

    def determine_consonant(self, x):
        if x in fricative2plosive:
            return "f"
        else:
            return ""

    def get_radical(self, x):
        return fricative2plosive[x] if x in fricative2plosive else x

    def parse_verb(self, verb):
        # get possible verbs sorted in order of shortest suffix-less form
        possibilities = sorted(self.match_morphemes(dict=self.verb_endings, string=verb), key=lambda x:len(x[2]))
        for (affix, word, stem, parse) in possibilities[:1]:
            print((affix, word, stem, parse))
            skeleton = self.get_skeleton(stem)
            patterns = self.match_morphemes(dict=self.patterns, string=skeleton, morpheme_type="skeleton")
            print(stem + "\t" + skeleton)
            for p in patterns:
                print(p)
        #skeleton = self.get_skeleton(verb)

    def parse_noun(self, noun):
        pass

    def match_morpheme(self, morpheme, string):
        '''
        :param affix: prefix, suffix or circumfix
        :param string:
        :return: determines if string has this affix
        '''
        return(bool(re.fullmatch(pattern=morpheme, string=string)))

    def remove_affix(self, affix, string):
        '''
        :param affix:
        :param string:
        :return: returns string with affix removed from it
        '''
        return re.sub(pattern=affix, string=string, repl='\g<1>')

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
            if self.match_morpheme(morpheme=morpheme, string=string):
                if morpheme_type == "affix":
                    value.append((morpheme, string, self.remove_affix(morpheme, string), "_".join(path)))
                elif morpheme_type == "skeleton":
                    value.append((morpheme, string, "_".join(path)))
            return(value)

        elif (type(dict) == list):
            values = []
            for morpheme in dict:
                if self.match_morpheme(morpheme=morpheme, string=string):
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

if __name__ == '__main__':
    P = Parser()
    #print(P.get_skeleton(string))
    P.parse_verb("teḵtvin")
    possibilities = P.match_morphemes(dict=P.verb_endings, string="teḵtvin")