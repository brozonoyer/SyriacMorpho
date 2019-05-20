import os, re, json


suffixes = dict()
numbers = ['sing', 'pl']
vowels = 'āēaeiou'
endings = {'masc-pl': ['in', 'ay', 'ē'], 'fem-pl':['ān', 'āṯ', 'āṯā']}
to_double = ['āw', 'aw']
spirant_dict = {'v': 'b', 'f':'p', 'ṯ':'t', 'ḡ':'g', 'ḏ':'d'}

class NounFormsGenerator():


    def __init__(self, gender):
        self.gender = gender
        self.absolute = {'sing': [], 'pl': []}
        self.construct = {'sing': [], 'pl': []}
        self.emphatic = {'sing': [], 'pl': []}
        self.stems = []
        self.forms = [self.absolute, self.construct, self.emphatic]
        self.form_dict = {'abs': self.absolute, 'cons': self.construct, 'emph': self.emphatic}
    # def insert(self, number, insertion, endings):


    def add(self, number, to_add):
        if number in numbers:
            for form in self.forms:
                form[number].append(self.stems[0] + to_add)
        elif number.startswith('emph'):
            self.emphatic['pl'].append(self.stems[0] + to_add)

    def insert(self, number, to_insert, to_add):
        if number in numbers:
            index = 0
            if to_insert in to_double:
                last_letter = to_insert[-1]
                to_insert = to_insert + last_letter
            elif len(to_insert) == 1 and self.stems[0][-2] == self.stems[0][-1]:
                self.stems[0] = self.stems[0][:-1]
            for form in self.forms:
                form[number].append(self.stems[0] + to_insert + endings[to_add][index])
                index += 1
        elif number.startswith('emph'):
            self.emphatic['pl'].append(self.stems[0] + to_insert + endings[to_add][2])

    def irr(self, number, irregular_forms):
        if type(irregular_forms) == list:
            index = 0
            for form in self.forms:
                form[number].append(irregular_forms[index])
                index += 1
        else:
            numbers = number.split('-')
            form_dict = self.form_dict[numbers[0]]
            nr = numbers[1]
            form_dict[nr].append(irregular_forms)

    def delete(self, number, to_delete):
        del_length = len(to_delete)
        index = 0-del_length
        if number in numbers:
            for form in self.forms:
                form[number].append(self.stems[0][:index])
        elif number.startswith('emph'):
            self.emphatic['pl'].append(self.stems[0][:index])

    def replace(self, number, to_replace, to_add):
        del_length = len(to_replace)
        index = 0-del_length
        dict_i = 0
        if number in numbers:
            for form in self.forms:
                if to_add in endings.keys():
                    form[number].append(self.stems[0][:index] + endings[to_add][dict_i])
                else:
                    form[number].append(self.stems[0][:index] + to_add)
                dict_i += 1
        elif number.startswith('emph'):
            self.emphatic['pl'].append(self.stems[0][:index] + to_add)

    def swap(self, number, from_val, to_val, swap_endings):
        from_index = self.stems[0].index(from_val)
        to_index = self.stems[0].index(to_val)
        stem_list = list(self.stems[0])
        stem_list[from_index], stem_list[to_index] = stem_list[to_index], stem_list[from_index]
        stem = ''.join(stem_list)
        dict_i = 0
        if number in numbers:
            for form in self.forms:
                form[number].append(stem + endings[swap_endings][dict_i])
                dict_i += 1
        elif number.startswith('emph'):
            self.emphatic['pl'].append(stem + endings[swap_endings][2])

    def all_same(self):
        for form in self.forms:
            for key in form:
                form[key].append(self.stems[0])

    def clean(self):
        self.absolute['sing'] = sorted(list(set(self.absolute['sing'])))
        self.construct['sing'] = sorted(list(set(self.construct['sing'])))
        self.emphatic['sing'] = sorted(list(set(self.emphatic['sing'])))
        self.absolute['pl'] = sorted(list(set(self.absolute['pl'])))
        self.construct['pl'] = sorted(list(set(self.construct['pl'])))
        self.emphatic['pl'] = sorted(list(set(self.emphatic['pl'])))


if __name__ == '__main__':
    file_name = os.path.join(os.path.curdir, 'lexicon/nouns.tsv')
    file = open(file_name)
    words = dict()
    for line in file.readlines():
        word_dict = dict()
        noun = re.sub(r'[\s\t]+[m/f]+[\s\t]+.+\n', '', line)
        gender = re.sub(r'^[’‘\wāē]+[\s\t]+', '', line)
        gender = re.sub(r'[\s\t]+.+\n', '', gender)
        operations = re.sub(r'^[’‘\wāē]+[\s\t]+[m/f]+[\s\t]+', '', line)
        operations = re.sub('\n', '', operations)
        operations = re.sub(r',', ';', operations)
        operations = re.sub(r':', ',', operations)
        operations = re.sub(r'[\)\[\]]', '', operations)
        operations = re.sub(r'\(', ', ', operations)
        operations = operations.split('; ')
        # with open(os.path.join(os.path.curdir, 'declension.json'), 'r') as f:
        #    json_dict = json.load(f)

        generator = NounFormsGenerator(gender)
        print(generator.gender)
        generator.emphatic['sing'].append(noun)
        masc_stem = ""
        fem_stem = ""
        if 'masc-sing' in operations:
            generator.stems.append(noun[:-1])
            masc_stem = noun[:-1]
            if masc_stem[-2] == masc_stem[-1]:
                masc_stem = masc_stem[:-1]
            masc_stem = re.sub(r'[u|o]', 'w', masc_stem)
            masc_stem = re.sub(r'i', 'y', masc_stem)
            masc_stem = re.sub(r'rr', 'r', masc_stem)
            masc_stem = re.sub(r'll', 'l', masc_stem)
            masc_stem = re.sub(r'zz', 'z', masc_stem)
            absolute_const = [l for l in masc_stem if l not in vowels]
            new_list = []
            for a in absolute_const:
                new_list.append(spirant_dict[a] if a in spirant_dict.keys() else a)
            abs_const = ''.join(new_list)
            generator.absolute['sing'].append(abs_const)
            generator.construct['sing'].append(abs_const)
        if 'fem-sing' in operations:
            poss_stem = noun[:-2]
            if poss_stem[-1] in vowels:
                poss_stem = noun[:-3]
            generator.stems.append(poss_stem)
            generator.absolute['sing'].append(poss_stem + 'ā')
            generator.construct['sing'].append(poss_stem + 'aṯ')
            fem_stem = poss_stem
        if noun[-1] not in vowels:
            generator.stems.append(noun)
        elif (noun.endswith('tā') or noun.endswith('ṯā')) and not generator.stems:
            poss_stem = noun[:-2]
            if poss_stem[-1] in vowels:
                poss_stem = noun[:-3]
            generator.stems.append(poss_stem)
        elif not generator.stems:
            generator.stems.append(noun[:-1])

        if 'masc-pl' in operations:
            generator.absolute['pl'].append(generator.stems[0] + 'in')
            generator.construct['pl'].append(generator.stems[0] + 'ay')
            generator.emphatic['pl'].append(generator.stems[0] + 'ē')
        if 'fem-pl' in operations:
            generator.absolute['pl'].append(generator.stems[0] + 'ān')
            generator.construct['pl'].append(generator.stems[0] + 'āṯ')
            generator.emphatic['pl'].append(generator.stems[0] + 'āṯā')
        generator.stems = list(set(generator.stems))
        print(noun + ":__:" + gender + ":__:" + str(operations))
        for operation in operations:
            elements = operation.split(', ')
            if operation.startswith('add'):
                generator.add(elements[1], elements[2])
            elif operation.startswith('insert'):
                generator.insert(elements[1], elements[2], elements[3])
            elif operation.startswith('irr'):
                if len(elements) > 4:
                    irr_element = elements[2:]
                else:
                    irr_element = elements[2]
                generator.irr(elements[1], irr_element)
            elif operation.startswith('delete'):
                generator.delete(elements[1], elements[2])
            elif operation.startswith('replace'):
                generator.replace(elements[1], elements[2], elements[3])
            elif operation.startswith('swap'):
                generator.swap(elements[1], elements[2], elements[3], elements[4])
        word_dict['stem'] = generator.stems[0]
        word_dict['absolute_sing'] = generator.absolute['sing']
        word_dict['absolute_pl'] = generator.absolute['pl']
        word_dict['construct_sing'] = generator.construct['sing']
        word_dict['construct_pl'] = generator.construct['pl']
        word_dict['emphatic_sing'] = generator.emphatic['sing']
        word_dict['emphatic_pl'] = generator.emphatic['pl']
        word_dict['gender'] = generator.gender
        if 'all-forms' in operations:
            generator.all_same()

        generator.clean()

        print(noun)
        words[noun] = word_dict

    with open(os.path.join(os.path.curdir, 'word_declensions.json'), 'w') as f:
        json.dump(words, f, ensure_ascii=False)


