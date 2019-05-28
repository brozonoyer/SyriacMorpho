import re
from segment import Segment
from inventory import Inventory, abbreviations
from queue import LifoQueue as stack

class Rule():

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def __init__(self, rule_string, inventory_path='./inventory'):
        self.target, self.change, self.environment = self.parse_rule(rule_string=rule_string)

        self.inventory = Inventory(inventory_path=inventory_path)
        self.brackets = {'(': ')', '[': ']', '{': '}'}

        self.target_regex = self.target2regex()
        self.environment_regex = self.environment2regex(string=self.environment)
        self.rule_regex = self.rule2regex()

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def parse_rule(self, rule_string):
        '''
        :param rule_string: phonological rule, standard representation TARGET –> CHANGE / ENVIRONMENT
        :return: parsed into 3 parts: TARGET, CHANGE, ENVIRONMENT
        '''
        rule = rule_string.split('/')[0]
        target = rule.split('–>')[0].strip()
        change = rule.split('–>')[1].strip()
        environment = rule_string.split('/')[1].strip()
        return target, change, environment

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def apply(self, input):

        match = re.search(pattern=self.rule_regex, string=input)

        if not match:
            print('no environment for rule to apply')
            return input

        left_environment = match.group('left') # everything to the left of target
        right_environment = match.group('right')  # everything to the right of target
        target = match.group('target') # target callback group

        if self.change[0] == '[' or self.change in abbreviations: # if feature representation or C,V etc.
            S = Segment(representation=target, inventory=self.inventory)
            replacement = S.change_feature(feature=self.change)
        elif self.change == 'ø': # if deletion
            replacement = ''
        else: # if replacing with a segment
            replacement = self.change

        replacement_string = left_environment + replacement + right_environment

        output = re.sub(pattern=self.rule_regex, repl=replacement_string, string=input, count=1)
        return output

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def rule2regex(self):
        '''
        :return: put the named callback group for target into the _ slot of environment
        '''

        index_ = self.environment_regex.index('_')

        environment_regex_grouped = self.environment_regex[0]
        environment_regex_grouped += '(?P<left>'
        environment_regex_grouped += self.environment_regex[1:index_]
        environment_regex_grouped += ')_(?P<right>'
        environment_regex_grouped += self.environment_regex[index_+1:-1]
        environment_regex_grouped += ')'
        environment_regex_grouped += self.environment_regex[-1]

        self.environment_regex = environment_regex_grouped

        rule_regex = self.environment_regex.replace('_', self.target_regex)
        return rule_regex

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def target2regex(self):
        '''
        Converts target of rule to regex, placed in a callback group named "target"
        :return:
        '''
        target_group = self.environment2regex(string=self.target)
        target_group = '(?P<target>' + target_group + ')'
        return target_group

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def environment2regex(self, string):
        '''
        :param string: phonological environment
        :return:
        '''

        if string == 'ø':
            return ''

        regex = '(' # start regex capture group

        s = stack()
        i = 0

        while i < len(string):
            if string[i] == '[' and s.empty(): # if features, e.g. [-sonorant,+continuant]

                #print("CASE 1")

                # get feature string
                j = i+1
                while string[j] != ']':
                    j += 1
                r = string[i:j+1] # bracketed material

                # parse string in brackets
                regex += self.representation2regex(r)
                i = j + 1

            elif string[i] == '_': # _ denotes position, used only when parsing change as placeholder

                #print("CASE 2")

                regex += string[i]
                i += 1

            elif string[i] == '#': # anchoring environment to the beginning or end of word

                # print("CASE 3")

                if i == 0:
                    regex += '^'
                elif i == len(string)-1:
                    regex += '$'
                else:
                    raise Exception('# can only occur word-initially or word-finally')

                i += 1

            elif string[i] in {'{','('}: # if opening { or [ bracket

                #print("CASE 4")

                s.put((string[i], i))
                i += 1

            elif string[i] in {'}',')'}: # if closing } or ] bracket

                #print("CASE 5")

                (last_open_bracket, last_open_bracket_idx) = s.get()

                if string[i] != self.brackets[last_open_bracket]: # must correspond to opening bracket on top of stack
                    raise Exception('improper nesting of brackets')

                if not s.empty():
                    i += 1
                    continue

                r = string[last_open_bracket_idx:i+1] # get whatever's enclosed in parentheses, parentheses included

                if string[i] == ')':
                    print(r)
                    regex = regex + self.environment2regex(r[1:-1]) + '{0,1}' # recursive call on what's inside ()
                elif string[i] == '}':
                    regex += self.options2regex(r)

                i += 1

            elif s.empty(): # if single character not inside any brackets

                #print("CASE 6")

                r = string[i]
                regex += self.representation2regex(r)
                i += 1

            else: # character inside brackets

                #print("CASE 7")

                i += 1

        regex += ')'

        return regex

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def representation2regex(self, representation):
        '''
        :param feat: string in the form of C, V, or [+feat]
        :return: options of segments for that feature
        '''

        #segments = Segment(representation=representation, inventory=self.inventory).segments
        #print("representation", representation)
        segments = ''.join(self.inventory.get_segments_from_representation(representation=representation))
        return '[' + segments + ']'

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def options2regex(self, string):
        '''
        :param string: of form {C,V}
        :return: regex for options: [ptk]|[iao]
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
        :return: string split by commas, respecting brackets: e.g. (a,(b,c,d)),(e,f) will be split into 2 groups
        '''

        comma_separated = list()
        s = stack()

        i = 0
        curr_block = ''
        while i < len(string):

            if string[i] in self.brackets.keys(): # if opening bracket
                s.put(string[i])
                curr_block += string[i]

            elif string[i] in self.brackets.values(): # if closing bracket
                last_open_bracket = s.get()
                if string[i] != self.brackets[last_open_bracket]: # must correspond to opening bracket on top of stack
                    raise Exception('improper nesting of brackets')
                curr_block += string[i]

            elif string[i] == ',' and s.empty(): # if un-nested comma – actual separator
                comma_separated.append(curr_block)
                curr_block = ''

            else: # if character
                curr_block += string[i]

            i += 1

        comma_separated.append(curr_block)

        return comma_separated

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#


if __name__ == '__main__':
    #R= Rule(rule_string='{a,e,o} –> ø / C_C{VC,[+syllabic,+long]}')
    #R = Rule(rule_string='a –> ø / C_C')
    R = Rule(rule_string='ø –> i / #_Co')
    print(R.apply(input='kotba'))
