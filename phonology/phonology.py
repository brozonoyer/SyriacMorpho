import re
from copy import deepcopy
from phonology.rule import Rule
from phonology.segment import Segment
from phonology.pattern import Pattern


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


if __name__ == '__main__':

    P = Phonology()

    #Pa = Pattern(pattern="e_2_1_a_2_2f_3f",inventory=P.inventory)
    #print(Pa.regex)
    #print(Pa.match(string='etkatṯv'))
    #skel = Pa.make_skeleton('etkatṯv')
    #print(skel)
    #print(Pa.pattern2regex(skel))
    #print(Pa.match(string=Pa.pattern2regex(pattern=skel)))
    #print(Pa.get_corresponding_plosive_or_fricative('t'))
    #print(Pa.parse_segment('2'))
    #print(Pa.parse_segment('2f'))


    #R = Rule(rule_string='{a,e,o} –> ø / C_C{VC,[+syllabic,+long]}', inventory=P.inventory)
    #R = Rule(rule_string='e –> a / _{r,[+guttural]}', inventory=P.inventory)
    #print("rule\t"+R.rule_regex)
    #print("target\t"+R.target_regex)
    #print("change\t"+R.change)
    #print("enviro\t"+R.environment_regex)

    #print(R.apply('idatā'))
