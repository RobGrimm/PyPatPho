import os
import pickle
import time
from xlrd import open_workbook



""" Hacked-together script that goes through the MRC XLS file and extracts phonological represenations of nouns, verbs, adjectives.
Stores the resuls in a dict and pickles it to file. Requires MRC database: http://www.psych.rl.ac.uk/Word_data.zip """


start_time = time.time()


def get_file_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_orthographic(row):
    return row[-4].lower()


def get_phonemes(row):
    return row[-3].translate(None, '/')


# for converting MRC POS tags to a different format (I'm only using this for idiosyncratic personal reasons)
pos_dict = {'N': 'n',
        'J': 'adj',
        'V': 'v'}


# a lexeme is a word's orthographic representation (I think this is the lamme, the MRC documntation is not clear on this)
# together with its POS tag, e.g. 'car-n' for the noun 'car'
lexeme_dict = dict()

# get this from: http://www.psych.rl.ac.uk/Word_data.zip
workbook = open_workbook(get_file_path() + '/Word_data.xlsx')

for s in workbook.sheets():

    # go through the rows
    for row in range(s.nrows):

        # get the row as a list 'values'
        values = []
        for col in range(s.ncols):

            value = s.cell(row, col).value

            # skip the row if you encounter unicode trouble (not usually important)
            try:
                values.append(str(value))
            except UnicodeEncodeError:
                print 'unicode trouble!'
                print value

        # for the current row, get the orthographic word form, the POS tag ('pdwtype'),
        # and the phonological representation
        # skip the row if it is incomplete
        try:
            word = get_orthographic(values)
            pdwtype = values[-10]
            phonemes = get_phonemes(values)
        except IndexError:
            print values
            continue

        # skip the row if is orthographic word form, POS tag, or phoneme is the empty string
        if word == '' or pdwtype == '' or phonemes == '':
            continue

        # skip the row if it descibes a word whose POS tag we are not interested in
        if pdwtype not in pos_dict:
            continue

        # add phonological representation to lexeme dict
        lexeme = word + '-' + pos_dict[pdwtype]
        lexeme_dict[lexeme] = phonemes



pickle.dump(lexeme_dict, open(get_file_path() + '/mrc_dict.p', "wb"))


print "--- Done. This took %s minutes ---" % ((time.time() - start_time) / float(60))

print 'Extracted %s words.' % len(lexeme_dict) # 33.938 nouns, verbs and adjectives