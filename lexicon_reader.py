import os, re



if __name__== '__main__':
    file_name = os.path.join(os.path.curdir, 'lexicon/nouns.tsv')
    file = open(file_name)
    for line in file.readlines():
        noun = re.sub(r'[\s\t]+[m/f]+[\s\t]+.+\n', '', line)
        gender = re.sub(r'^[’‘\wāē]+[\s\t]+', '', line)
        gender = re.sub(r'[\s\t]+.+\n', '', gender)
        operations = re.sub(r'^[’‘\wāē]+[\s\t]+[m/f]+[\s\t]+', '', line)
        operations = re.sub(r',', ';', operations)
        operations = re.sub(r':', ',', operations)

        print(noun + ":__:" + gender + ":__:" + operations)

