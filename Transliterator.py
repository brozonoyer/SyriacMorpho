import os, json, unicodedata
from collections import defaultdict

class Transliterator():

    def __init__(self):
        self.together = {"\u0741","\u0742", "\u073C","\u073F", "\u0323"}
        with open('syriac_transl.json', 'r') as f:
            self.dict = json.load(f)

    def transliterate(self, syr):
        '''
        :param syr: word in Syriac
        :return: transliterated
        '''
        result = []
        for i, letter in enumerate(syr):
            print("––––––––––––––––––––––––––––––––––")
            print(i, 'U+%04x' % ord(letter), result)
            if syr[i] in self.together:
                result[-1] = self.dict[syr[i-1:i+1]]
            else:
                result.append(self.dict[letter])
            print(i, 'U+%04x' % ord(letter), result)

        return ''.join(result)


if __name__ == '__main__':
    T = Transliterator()
    #simplified = T.transliterate("ܕܚܸܫܘܿܟ̣ܝܢ")
    #print(simplified)
    #transliterated = T.transliterate("ܘܲܢܓܲܕܼ ܐܲܝܬ݁ܝܼ ܡܓ̣ܘܼ̈ܫܹܐ")
    transliterated = T.transliterate("ܕܒܲܣܢܝܼܩܘܼܬܹܗ")
    #transliterated = T.transliterate("ܕܲܦܬܲܟ̣ܪܘܼܬܼܵܐ")
    print(transliterated)
'''
    ܕ  d
    ܚ  hdot
    ܸ   e
    ܫ shin
    ܘ waw
    ܿ waw-over
    ܟ̣ܝܼܢ
'''