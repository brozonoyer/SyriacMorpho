
class Inventory():

    def __init__(self, inventory_path='./inventory'):
        self.inventory = self.load_inventory(inventory_path=inventory_path)

    def load_inventory(self, inventory_path='./inventory'):
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

if __name__ == '__main__':
    I = Inventory()