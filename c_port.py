# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:54:27 2015

@author: stephantulkens
"""

vowels = ['I','e','E','@','&','3','V','a','u','U','O','A','i']


def translate_left(word):
    """wrapper function for the left translation"""

    return translate(word)


def translate_right(word):
    """wrapper function for the right translation, which is just the left translation
but with reversed input and output"""

    return translate(word[::-1])[::-1]


def translate(word):
    """translation function, ugly C-like code, but it works!"""

    word = [Phoneme(x) for x in word]

    output = []
    x = 0

    while x < len(word):

        if word[x].isvowel:

            try:
                if len(output[-1]) == 2:
                    output.append([' ', ' ', ' '])
                if word[x+1].isvowel:
                    output.append([word[x].phoneme, word[x+1].phoneme])
                    x += 1
                else:
                    output.append([word[x].phoneme, ' '])
            except IndexError:
                output.append([word[x].phoneme, ' '])

        else:

            try:
                if len(output[-1]) == 3:
                    output.append([' ', ' '])
            except IndexError:
                pass
            try:
                if not word[x+1].isvowel:
                    try:
                        if not word[x+2].isvowel:
                            output.append([word[x].phoneme, word[x+1].phoneme, word[x+2].phoneme])
                            x += 2
                        else:
                            output.append([word[x].phoneme, word[x+1].phoneme, ' '])
                            x += 1
                    except IndexError:
                        output.append([word[x].phoneme, word[x+1].phoneme, ' '])
                        x += 1
                else:
                    output.append([word[x].phoneme, ' ', ' '])
            except IndexError:
                output.append([word[x].phoneme, ' ', ' '])

        x += 1

    intermediate = "".join(["".join(l) for l in output])
    intermediate += "".join([" " for nr in range(18 - len(intermediate))])

    return "".join(intermediate)


def translation_to_num_vector(translation):

    transdict = {'i': " 0.100 0.100  0.100", 'I': " 0.100 0.100  0.185", 'e': " 0.100 0.100  0.270", 'E': " 0.100 0.100  0.355",'&': " 0.100 0.100  0.444",'@': " 0.100 0.175  0.185",'3': " 0.100 0.175  0.270",'V': " 0.100 0.175  0.355",'a': " 0.100 0.175  0.444",'u': " 0.100 0.250  0.100",'U': " 0.100 0.250  0.185",'O': " 0.100 0.250  0.270",'o': " 0.100 0.250  0.355",'A': " 0.100 0.250  0.444",'p': " 1.000 0.450  0.733",'t': " 1.000 0.684  0.733",'k': " 1.000 0.921  0.733",'b': " 0.750 0.450  0.733",'d': " 0.750 0.684  0.733",'g': " 0.750 0.921  0.733",'m': " 0.750 0.450  0.644",'n': " 0.750 0.684  0.644",'N': " 0.750 0.921  0.644",'l': " 0.750 0.684  1.000",'r': " 0.750 0.684  0.911",'f': " 1.000 0.528  0.822",'v': " 0.750 0.528  0.822",'s': " 1.000 0.684  0.822",'z': " 0.750 0.684  0.822",'S': " 1.000 0.762  0.822",'Z': " 0.750 0.762  0.822",'j': " 0.750 0.841  0.911",'x': " 1.000 0.921  0.822",'h': " 1.000 1.000  0.911",'w': " 0.750 0.921  0.911",'T': " 1.000 0.606  0.822",'D': " 0.750 0.606  0.822",'C': " 1.000 0.841  0.822",'J': " 0.750 0.841  0.822"}

    return "".join([transdict.get(x, " 0.000 0.000 0.000") for x in translation])


def translation_to_binary_vector(translation):

    transdict = {"i": [0, 1, 0, 1, 1], "I": [0, 1, 0, 0, 1], "e": [0, 1, 1, 0, 1], "E": [0, 1, 1, 1, 0],
                 "&": [0, 1, 1, 0, 0], "@": [1, 1, 1, 0, 0], "3": [1, 1, 0, 0, 1], "V": [1, 1, 1, 1, 0],
                 "a": [1, 1, 1, 0, 0], "U": [1, 0, 0, 1, 1], "u": [1, 0, 0, 0, 1], "O": [1, 0, 1, 0, 1],
                 "Q": [1, 0, 1, 1, 0], "A": [1, 0, 1, 0, 0], "p": [0, 0, 0, 0, 0, 1, 0], "t": [0, 0, 1, 1, 0, 1, 0],
                 "k": [0, 1, 1, 0, 0, 1, 0], "b": [1, 0, 0, 0, 0, 1, 0], "d": [1, 0, 1, 1, 0, 1, 0],
                 "g": [1, 1, 1, 0, 0, 1, 0], "m": [1, 0, 0, 0, 0, 0, 1], "n": [1, 0, 1, 1, 0, 0, 1],
                 "N": [1, 1, 1, 0, 0, 0, 1], "l": [1, 0, 1, 1, 0, 1, 1], "r": [1, 0, 1, 1, 1, 1, 0],
                 "f": [0, 0, 0, 1, 1, 0, 0], "v": [1, 0, 0, 1, 1, 0, 0], "s": [0, 0, 1, 1, 1, 0, 0],
                 "z": [1, 0, 1, 1, 1, 0, 0], "S": [0, 1, 0, 0, 1, 0, 0], "Z": [1, 1, 0, 0, 1, 0, 0],
                 "j": [1, 1, 0, 1, 0, 1, 1], "h": [0, 1, 1, 1, 0, 1, 1], "w": [1, 1, 1, 0, 0, 1, 1],
                 "T": [0, 0, 1, 0, 1, 0, 0], "D": [1, 0, 1, 0, 1, 0, 0], "C": [0, 1, 0, 1, 1, 0, 0],
                 "J": [1, 1, 0, 1, 1, 0, 0]}
    output = []

    for x, y in enumerate(translation):
        try:
            output.extend(transdict[y])
        except KeyError:
            if x % 5 >= 3:
                output.extend([0, 0, 0, 0, 0])
            else:
                output.extend([0, 0, 0, 0, 0, 0, 0])

    return output


class Phoneme:
    """phoneme helper class"""

    def __init__(self, phoneme):

        self.isvowel = phoneme in vowels
        self.phoneme = phoneme

    def __repr__(self):

        return self.phoneme



if __name__ == "__main__":


    # some test cases, phonological represntations taken from MRC

    v1 = translation_to_binary_vector(translate('@Uld')) # adejctive 'old'
    v2 = translation_to_binary_vector(translate('weIt')) # verb 'wait'
    v3 = translation_to_binary_vector(translate('hI@')) # verb 'hear'

    print len(v1), v1 # this is incorrecttly aligned with the metricla grid, plust the vector has length 112 (should be 114)
    print len(v2), v2
    print len(v3), v3
