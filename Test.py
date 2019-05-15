import unittest
from Parser import Parser
from phonology.phonology import Phonology, Rule

class Test(unittest.TestCase):

    def test_verbs(self):
        P = Parser()
        self.assertEqual(P.parse_verb('neṯkatvān')[0], 'Ethpaal_finite_imperfect_pl_3_f')
        self.assertEqual(P.parse_verb('’aḵtvaṯ')[0], 'Afel_finite_perfect_sg_3_f')
        self.assertEqual(P.parse_verb('kṯav')[0], 'Peal_finite_perfect_sg_3_m')

    def test_rules(self):
        P = Phonology(inventory_path='./phonology/inventory', rules_path='./phonology/rules')
        R = Rule(rule_string='{a,e,o} –> ø / C_C{VC,[+syllabic,+long]}', inventory=P.inventory)
        self.assertEqual(R.apply('idotal'), 'idtal')

    def test_nouns(self):
        P = Parser()

if __name__ == '__main__':
    unittest.main()