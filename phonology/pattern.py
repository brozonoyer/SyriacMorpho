
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
