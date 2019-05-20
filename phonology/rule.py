from phonology.rule import Rule
from phonology.segment import Segment
from phonology.pattern import Pattern

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
