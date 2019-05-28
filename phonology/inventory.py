
abbreviations = {'V':'[+syllabic]', # vowel
                 'C':'[-syllabic]', # consonant
                 'G':'[-syllabic,+approximant]', # glide
                 'L':'[+approximant,+consonantal]', # liquid
                 'N':'[+nasal]', # nasal
                 'O':'[-sonorant]', # obsruent
                 'T':'[-sonorant,-continuant]',  # plosive
                 'F':'[-sonorant,+continuant]'}  # fricative

values = {'+','-','@','&'} # @ = alpha, & = beta (variables)

class Inventory():

    def __init__(self, inventory_path='./inventory'):
        self.inventory = self._load_inventory(inventory_path=inventory_path)
        self.segments = set(self.inventory.keys())
        self.features = set(self.inventory[list(self.inventory.keys())[0]].keys())
        self.consonants = set(self.get_segments_from_representation('[-syllabic]'))
        self.vowels = set(self.get_segments_from_representation('[+syllabic]'))

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def _load_inventory(self, inventory_path='./inventory'):
        '''
        :param path:
        :return:
        '''

        with open(inventory_path, 'r') as f:
            segments = [s.strip().split() for s in f.readlines()]

        feature_types = segments[0][1:]
        segment_list = segments[1:]

        inventory = {}
        for s in segment_list:
            segment = s[0]
            segment_dict = {}
            for i, value in enumerate(s[1:]):
                segment_dict[feature_types[i]] = value
            inventory[segment] = segment_dict

        return inventory

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def get_segments_from_representation(self, representation):
        '''
        :param feat_string: represents segments, e.g. '[-syllabic]' or 'C' or just 'k'
        :return: list of all segments of this type in the inventory
        '''
        segments = list()

        if self._is_feat(representation) or representation in abbreviations:
            feat_dict = self._parse_feat_string(representation)
            for s in self.inventory: # goes through segments in inventory and checks if they have features of feat_string
                if feat_dict.items() <= self.inventory[s].items():
                    segments.append(s)
            return segments

        elif representation in self.segments: # if string is just a segment
            segments.append(representation)
            return segments

        elif representation == 'ø':
            return segments

        else:
            raise Exception("invalid representation: %s" % representation)

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def _parse_feat_string(self, feat_string):
        '''
        :param feat_string: of form [-sonorant,-continuant], or T (abbreviation)
        :return: feat_dict: of form {sonorant:-, continuant:-}
        '''
        if feat_string in abbreviations:
            feat_string = abbreviations[feat_string]
        feats = feat_string[1:-1].split(',')
        feat_dict = dict()
        for f in feats:
            feat_dict[f[1:]] = f[0]
        return feat_dict

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def _is_feat(self, string):
        '''
        :param string:
        :return: True if string is of form [+sonorant]
        '''
        is_feat = False
        if len(string) > 1 and string[0] == '[' and string[1] in values and string[-1] == ']':
            is_feat = True
        return is_feat

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#


if __name__ == '__main__':
    I = Inventory()
    print(I.inventory)
    print(I.segments)
    print(I.features)
    #print(I.parse_feat_string(feat_string='[+syllabic,@nasal,+sonorant]').items())
    print(I.get_segments_from_representation('[-syllabic,+nasal,-coronal]'))