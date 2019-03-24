import os, json
from collections import defaultdict

class Transliterator():

    def __init__(self):
        dict = json.loads('syriac_translit.json')
        print(dict)

    def syriac2latin(self):
        pass

    def latin2syriac(self):
        pass

if __name__ == '__main__':
    T = Transliterator()
    #print('ܕ' == '\u0715')