import re
from copy import deepcopy


vowel = {"u","o","a","ā","e","ē","i"}

consonant = {"’","b","v","g","ġ","d","ḏ","h","w","z","ḥ","ṭ","y","k","ḵ","l","m","n","s","‘","p","f","ṣ","q","r","š","t","ṯ"}

beghadhkephath = {"b","g","d","k","p","t"}

plosive2fricative = {"b":"v","g":"ġ","d":"ḏ","k":"ḵ","p":"f","t":"ṯ"}

fricative2plosive = {"v":"b","ġ":"g","ḏ":"d","ḵ":"k","f":"p","ṯ":"t"}

guttural = {"’","ḥ","‘"}

voiced = {"u","o","a","ā","e","ē","i","b","v","g","ġ","d","ḏ","w","z","y","l","m","n","r"}

obstruent = {"b","v","g","ġ","d","ḏ","k","ḵ","p","f","t","ṯ"}

nasal = {"m","n"}


#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

class Phonology():

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def __init__(self, inventory_path='./inventory', rules_path='./rules'):
        self.inventory = self.load_inventory(path=inventory_path)
        self.rules = self.parse_rules(path=rules_path)

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def load_inventory(self, path='./inventory'):
        '''
        :param path:
        :return:
        '''

        with open(path, 'r') as f:
            segments = [s.strip().split() for s in f.readlines()]

        feature_types = segments[0][1:]
        segment_list = segments[1:]
        inventory = {}
        for s in segment_list:
            segment = s[0]
            segment_dict = {}
            for i,value in enumerate(s[1:]):
                segment_dict[feature_types[i]] = value
            inventory[segment] = segment_dict

        return inventory

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def get_skeleton(self, string):
        '''
        :param string:
        :return: verbal skeleton of Cs and Vs
        '''
        skeleton = []
        num_Cs = 0
        for x in string:
            if x in vowel:
                skeleton.append(x)
            else:
                num_Cs += 1
                skeleton.append(str(num_Cs) + self.determine_consonant(x))
        return "_".join(skeleton)

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def syllabify(self, string):
        pass

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def determine_consonant(self, x):
        if x in fricative2plosive:
            return "f"
        else:
            return ""

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def get_radical(self, x):
        return fricative2plosive[x] if x in fricative2plosive else x

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def parse_rules(self, path='./rules'):
        with open(path, 'r') as f:
            rules = [self.parse_rule(r.strip()) for r in f.readlines()]
        return rules

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def parse_rule(self, rule_string):
        rule = rule_string.split('/')[0]
        target = rule.split('–>')[0].strip()
        change = rule.split('–>')[1].strip()
        environment = rule_string.split('/')[1].strip()
        return((target, change, environment))

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#


class Rule():

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def __init__(self, rule_string, inventory):
        self.target, self.change, self.environment = self.parse_rule(rule_string=rule_string)

        self.inventory = inventory
        self.brackets = {'(': ')', '[': ']', '{': '}'}

        self.target_regex = self.target2regex()
        self.environment_regex = self.environment2regex(string=self.environment)
        self.rule_regex = self.rule2regex()

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def parse_rule(self, rule_string):
        rule = rule_string.split('/')[0]
        target = rule.split('–>')[0].strip()
        change = rule.split('–>')[1].strip()
        environment = rule_string.split('/')[1].strip()
        return target, change, environment

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def apply(self, input):

        print("rule_regex", self.rule_regex)
        print("string", input)
        target = re.search(pattern=self.rule_regex, string=input).group('target')
        print("target", target)
        S = Segment(representation=target, inventory=self.inventory)

        if self.change[0] == '[' or self.change[0] == 'C' or self.change[0] == 'V':
            S.change_feature(feature=self.change)
            replacement = S.segments
        elif self.change == 'ø':
            replacement = ''
        else:
            replacement = self.change
        print("replacement", replacement)

        replaced = re.sub(pattern=target,repl=replacement,string=input)
        return replaced

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def rule2regex(self):
        '''
        :param rule: character-tokenized rule of form ['C','[+syllabic]', '{C,V}']
        :return:
        '''
        rule_regex = self.environment_regex.replace('_', self.target_regex)
        return rule_regex

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def target2regex(self):
        target_group = self.environment2regex(string=self.target)
        target_group = '(?P<target>' + target_group + ')'
        return target_group

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def environment2regex(self, string):

        regex = '('

        i = 0

        while i < len(string):
            if string[i] in self.brackets: # if bracketed material

                # get string in brackets
                j = i+1
                while string[j] != self.brackets[string[i]]:
                    j += 1
                r = string[i:j+1]

                # parse string in brackets
                if string[i] == '[':
                    regex += self.feats2regex(r)
                elif string[i] == '{':
                    regex += self.options2regex(r)
                elif string[i] == '(':
                    regex = regex + self.environment2regex(r) + '{0,1}'
                i = j+1

            elif string[i] == '_': # if _ denoting position
                regex += string[i]
                i += 1

            else: # if single character

                r = string[i]
                regex += self.feats2regex(r)
                i += 1

        regex += ')'

        return regex

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def feats2regex(self, feats):
        '''
        :param feat: string in the form of C, V, or [+feat]
        :return: options of segments for that feature
        '''

        segments = Segment(representation=feats, inventory=self.inventory).segments
        return '[' + segments + ']'

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def options2regex(self, string):
        '''
        :param string:
        :return:
        '''

        options = self.split_by_comma(string[1:-1])
        regex = '('

        # parse all options, connect by | operator
        regex += self.environment2regex(options[0])
        for o in options[1:]:
            regex += '|'
            regex += self.environment2regex(o)

        regex += ')'

        return regex

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def split_by_comma(self, string):
        '''
        :param string:
        :return: string split by commas, respecting brackets
        '''

        comma_separated = []

        i = 0
        curr_block = ''
        while i < len(string):

            if string[i] == ',': # if comma
                comma_separated.append(curr_block)
                curr_block = ''
                i += 1

            elif string[i] in self.brackets:  # if bracketed material

                # get string in brackets
                j = i + 1
                while string[j] != self.brackets[string[i]]:
                    j += 1
                curr_block += string[i:j + 1]
                i = j + 1

            else: # if character
                curr_block += string[i]
                i += 1

        comma_separated.append(curr_block)

        return comma_separated

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

class Segment():
    '''
    Manipulates segment or feature bundle
    '''

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def __init__(self, representation, inventory):
        self.inventory = inventory
        representation, is_segment = self.parse_representation(representation)
        if is_segment: # if segmental representation
            self.segments = representation
            self.feature_bundle = self.segment2bundle(representation)
        else: # if feature bundle representation
            self.feature_bundle = representation
            self.segments = self.bundle2segments(representation)

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def parse_representation(self, representation):
        '''
        :param representation: segment of form 's' or feature bundle of form [-syllabic,+voice]
        :return:
        '''

        is_segment = False

        if (representation[0] != '[' and representation != 'C' and representation != 'V') or representation == 'ø': # if it's a segment and not a feature
            is_segment = True
            return representation, is_segment

        if representation == 'C':
            representation = '[-syllabic]'
        elif representation == 'V':
            representation = '[+syllabic]'

        feats = representation[1:-1].split(',') # remove square brackets
        # parse through features within brackets, e.g. [+syllabic, +voiced, -sonorant]
        feature_bundle = dict()
        for f in feats:
            if f[0] == 'C':
                feature_bundle['syllabic'] = '-'
            elif f[0] == 'V':
                feature_bundle['syllabic'] = '+'
            else:
                feature_bundle[f[1:]] = f[0]

        return feature_bundle, is_segment

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def bundle2segments(self, feature_bundle):

        segments = ''

        # match every possible segment to feature bundle
        for segment in self.inventory:
            match = True
            for feat_type in feature_bundle:
                if self.inventory[segment][feat_type] != feature_bundle[feat_type]:
                    match = False
            if match:
                segments += segment

        return segments

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def segment2bundle(self, segment):
        return deepcopy(self.inventory[segment])

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def change_feature(self, feature):
        '''
        :param feature: required form: e.g. [+syllabic]
        :return:
        '''
        new_feature_bundle, is_bundle = self.parse_representation(feature)
        for feat in new_feature_bundle:
            self.feature_bundle[feat] = new_feature_bundle[feat]
        self.segments = self.bundle2segments(self.feature_bundle)


#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

class Pattern():

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def __init__(self, pattern, inventory):
        self.inventory = inventory
        self.digit2string = {'1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five',
                             '1f': 'one_f', '2f': 'two_f', '3f': 'three_f', '4f': 'four_f', '5f': 'five_f'}
        self.regex = self.pattern2regex(pattern)

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def match(self, string):
        return re.fullmatch(pattern=self.regex,string=string)

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def pattern2regex(self, pattern):

        if len(pattern) == 0:
            return ''

        segments = pattern.split("_")
        groups_encountered = set()
        regex = ''
        for segment in segments:
            #print(groups_encountered)
            parsed, groups_encountered = self.parse_segment(segment, groups_encountered=groups_encountered)
            regex += parsed
        return regex

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def parse_segment(self, segment, groups_encountered):

        if segment in groups_encountered:
            return '(?P=' + self.digit2string[segment] + ')', groups_encountered

        elif segment[0].isdigit(): # if representation of radical

            groups_encountered.add(segment)

            regex = '(?P<' + self.digit2string[segment] + '>['
            consonants = ''
            if len(segment) > 1: # if of form '1f' – fricative
                for s in self.inventory:
                    if self.inventory[s]['C'] == '+' and not (self.inventory[s]['sonorant'] == '-' and self.inventory[s]['continuant'] == '-'):
                        consonants += s
            else: # if of form '1' – plosive
                for s in self.inventory:
                    if self.inventory[s]['C'] == '+' and not (self.inventory[s]['sonorant'] == '-' and self.inventory[s]['continuant'] == '+'):
                        consonants += s
            regex = regex + consonants + '])'
            return regex, groups_encountered

        else: # if just segment
            return segment, groups_encountered

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def make_skeleton(self, string):
        skeleton = []
        Cs_encountered = dict()
        num_Cs = 0
        for x in string:
            if x in vowel:
                skeleton.append(x)
            else: # if consonant
                if x in Cs_encountered:
                    skeleton.append(str(Cs_encountered[x]) + self.determine_consonant(x))
                else:
                    num_Cs += 1
                    Cs_encountered[x] = num_Cs
                    Cs_encountered[self.get_corresponding_plosive_or_fricative(x)] = num_Cs
                    skeleton.append(str(Cs_encountered[x]) + self.determine_consonant(x))
        return "_".join(skeleton)

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def determine_consonant(self, x):
        if x in fricative2plosive:
            return "f"
        else:
            return ""

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def get_corresponding_plosive_or_fricative(self, x):
        s = Segment(representation=x, inventory=self.inventory)
        original = s.segments
        if s.feature_bundle['sonorant'] == '-' and s.feature_bundle['continuant'] == '-': # if plosive
            s.change_feature('[+continuant]')
            return s.segments
        elif s.feature_bundle['sonorant'] == '-' and s.feature_bundle['continuant'] == '+': # if fricative
            s.change_feature('[-continuant]')
            return s.segments
        else:
            return original

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#


#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

if __name__ == '__main__':

    #re.match('(?P=1[])')

    #s = r'ataa'
    #reg = r'([uoaāeēi](?P<target>([’bvgġdḏhwzḥṭykḵlmns‘pfṣqrštṯ]))[uoaāeēi])'
    #reg = re.compile(reg)
    #to_replace = re.match(reg,s).group('target')
    #rep = r'd'
    #result = re.sub(pattern=to_replace,repl=rep,string='ata')
    #print(result)


    P = Phonology()

    Pa = Pattern(pattern="e_2_1_a_2_2f_3f",inventory=P.inventory)
    print(Pa.regex)
    #print(Pa.match(string='etkatṯv'))
    skel = Pa.make_skeleton('etkatṯv')
    print(skel)
    print(Pa.pattern2regex(skel))
    #print(Pa.match(string=Pa.pattern2regex(pattern=skel)))
    #print(Pa.get_corresponding_plosive_or_fricative('t'))
    #print(Pa.parse_segment('2'))
    #print(Pa.parse_segment('2f'))


    print()

    #R = Rule(rule_string='{a,e,o} –> ø / C_C{VC,[+syllabic,+long]}', inventory=P.inventory)
    R = Rule(rule_string='{a,e,o} –> ø / C_C{VC,[+syllabic,+long]}', inventory=P.inventory)
    #R = Rule(rule_string='e –> a / _{r,[+guttural]}', inventory=P.inventory)
    print("rule\t"+R.rule_regex)
    print("target\t"+R.target_regex)
    print("change\t"+R.change)
    print("enviro\t"+R.environment_regex)

    print(R.apply('idatuk'))