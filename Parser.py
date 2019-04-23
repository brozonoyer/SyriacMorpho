import json, re

vowels = {"u","o","a","ā","e","ē","i"}

consonants = {"b","ḇ","g","ġ","d","ḏ","h","w","z","ḥ","ṭ","y","k","ḵ","l","m","n","s",
              "‘","p","f","ṣ","q","r","š","t","ṯ"}

beghadhkephath = {"b","g","d","k","p","t"}

plosives2fricatives = {"b":"ḇ",
                       "g":"ġ",
                       "d":"ḏ",
                       "k":"ḵ",
                       "t":"ṯ"}

class Parser():

    def __init__(self):
        with open("conjugation.json","r") as v:
            self.verb_endings = json.load(v)
        with open("declension.json","r") as n:
            self.noun_endings = json.load(n)

    def get_skeleton(self, string):
        '''
        :param string:
        :return: verbal skeleton of Cs and Vs
        '''
        return "".join(list(map(lambda x: "V" if x in vowels else "C", string)))

    def parse_verb(self, verb):
        possibilities = sorted(self.match_affixes(dict=self.verb_endings, string=verb),
                               key = lambda x: len(x[2]))
        for p in possibilities:
            print(p)
        #skeleton = self.get_skeleton(verb)

    def parse_noun(self, noun):
        possibilities = sorted(self.match_affixes(dict=self.noun_endings, string=noun),
                               key = lambda x: len(x[2]))
        for p in possibilities:
            print(p)
        pass

    def match_affix(self, affix, string):
        '''
        :param affix: prefix, suffix or circumfix
        :param string:
        :return: determines if string has this affix
        '''
        return(bool(re.fullmatch(pattern=affix, string=string)))

    def remove_affix(self, affix, string):
        '''
        :param affix:
        :param string:
        :return: returns string with affix removed from it
        '''
        return re.sub(pattern=affix, string=string, repl='\g<1>')

    def match_affixes(self, dict, string, path=[]):
        '''
        :param dict: [nested] dictionary of paradigms
        :param string: word to match
        :param path: to store grammatical values recursively
        :return: list of possibilities of form [(affix, string_original, string_stripped_of_affix, grammatical_value)]
        '''

        if (type(dict) == str):
            value = []
            affix = dict
            if self.match_affix(affix=affix, string=string):
                value.append((affix, string, self.remove_affix(affix, string), "_".join(path)))
            #print(value)
            return(value)

        elif (type(dict) == list):
            values = []
            for affix in dict:
                if self.match_affix(affix=affix, string=string):
                    value = (affix, string, self.remove_affix(affix, string), "_".join(path))
                    values.append(value)
            #print(values)
            return values

        else:
            possibilities = []
            for i, v in enumerate(dict.values()):
                path_prime = path.copy()
                path_prime.append(list(dict.keys())[i])
                possibilities.extend(self.match_affixes(v, string, path_prime))
            return possibilities


if __name__ == '__main__':
    P = Parser()
    #print(P.get_skeleton(string))
    P.parse_verb("teḵtvin")
    P.parse_noun("’arbabšabbē")
    P.parse_noun("’ūmmānin")
    #possibilities = P.match_affixes(dict=P.verb_endings, string="teḵtvin")
