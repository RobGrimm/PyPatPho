import os
import cPickle
import time
from collections import defaultdict
from xlrd import open_workbook


class MRCRepo(object):
    """class that represents the MRC database, organised by POS"""

    def __init__(self, lexemes):

        self.lexemes = lexemes

    def phonologicalform_word(self, word):

        for pos in self.lexemes.keys():

            try:
                return pos[word]
            except KeyError:
                continue
        return None

    def phonologicalform_pos(self, pos, word):

        try:
            return self.lexemes[pos][word]
        except KeyError:
            return None

    def allwordsbypos(self, pos):

        try:
            return self.lexemes[pos]
        except KeyError:
            return {}


""" Hacked-together script that goes through the MRC XLS file and extracts phonological represenations of nouns, verbs, adjectives.
Stores the resuls in a dict and pickles it to file. Requires MRC database: http://www.psych.rl.ac.uk/Word_data.zip """
def get_words_from_mrc(pathtodir, pos={'N': 'n', 'J': 'adj', 'V': 'v'}):

    start_time = time.time()

    # for converting MRC POS tags to a different format (I'm only using this for idiosyncratic personal reasons)
    pos_dict = pos

    print "Starting"
    # a lexeme is a word's orthographic representation (I think this is the lemma, the MRC documntation is not clear on this)
    # together with its POS tag, e.g. 'car-n' for the noun 'car'
    lexeme_dict = {}

    # get this from: http://www.psych.rl.ac.uk/Word_data.zip

    print "Opening workbook"
    workbook = open_workbook(pathtodir + "/Word_data.xlsx")
    print "Workbook opened"

    for s in workbook.sheets():

        # go through the rows
        # if a sheet has less than 10 columns there's no need to go through it as the code below will fail.
        if s.ncols < 10:
            continue
        for row in range(s.nrows):

            try:
                word = str(s.cell(row, s.ncols - 4).value).lower()
                pdwtype = str(s.cell(row, s.ncols - 10).value)
                # If the word has the wrong POS stop further computation.
                if pdwtype not in pos_dict:
                    continue
                phonemes = str(s.cell(row, s.ncols - 3).value).translate(None, '/')
            except UnicodeEncodeError:
                continue
            except IndexError:
                continue

            # skip the row if is orthographic word form, POS tag, or phoneme is the empty string
            if not (word and pdwtype and phonemes):
                continue

            # add phonological representation to lexeme dict

            lexeme_dict.setdefault(pos_dict[pdwtype], dict())[word] = phonemes
            '''lexeme_dict.setdefault(pdwtype, dict())[word] = phonemes'''

    print "--- Done. This took %s minutes ---" % ((time.time() - start_time) / float(60))

    print 'Extracted %s words.' % len(lexeme_dict) # 33.938 nouns, verbs and adjectives

    return MRCRepo(lexeme_dict)


if __name__ == "__main__":

    mrc = get_words_from_mrc(os.getcwd())
    cPickle.dump(mrc, open(os.getcwd() + '/mrc.p', "wb"))