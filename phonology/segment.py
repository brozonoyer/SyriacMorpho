from copy import deepcopy
from inventory import abbreviations

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
        :param representation: segment of form 's' or [-sonorant,-continuant]/T (abbreviation)
        :return: segment/feat_dict, is_segment: 's', True or {sonorant:-, continuant:-}, False, respectively
        '''

        is_segment = False

        if (representation[0] != '[' and representation not in abbreviations) or representation == 'ø': # if it's a segment and not a feature
            is_segment = True
            return representation, is_segment

        if representation in abbreviations:
            representation = abbreviations[representation] # convert to features

        feats = representation[1:-1].split(',') # remove square brackets

        # parse through features within brackets, e.g. [+syllabic, +voiced, -sonorant]
        feature_bundle = dict()
        for f in feats:
            feature_bundle[f[1:]] = f[0]

        return feature_bundle, is_segment

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def bundle2segments(self, feature_bundle):
        '''
        :param feature_bundle: dict of features and values
        :return: string of all segments matching whose features are a superset of feature_bundle
        '''

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
        return deepcopy(self.inventory.inventory[segment])

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

    def change_feature(self, feature):
        '''
        :param feature: required form: e.g. [+syllabic]
        :return: segment(s) derived from current segment by adding/changing feature value
        '''
        new_feature_bundle, is_segment = self.parse_representation(feature)
        for feat in new_feature_bundle:
            self.feature_bundle[feat] = new_feature_bundle[feat]
        self.segments = self.bundle2segments(self.feature_bundle)
        return self.segments
