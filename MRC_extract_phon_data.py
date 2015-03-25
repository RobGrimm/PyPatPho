import os
import cPickle
import time
from xlrd import open_workbook


class MRCRepo(object):
    """class that represents the MRC database, organised by POS"""

    def __init__(self, lexemes):

        self.lexemes = lexemes


    def phonologicalform_wtype(self, pos, word):
        """ get the phonological form of a word for a specific POS tag """
        try:
            phonemes = self.lexemes['WTYPE'][pos][word]
            return phonemes
        except KeyError:
            return None


    def phonologicalform_pdwtype(self, word):
        """ get the phonological form of a word, for its most common POS tag (returns POS tag as well) """
        try:
            phonemes, pos = self.lexemes['PDWTYPE'][word]
            return phonemes, pos
        except KeyError:
            return None, None


    def phonologicalform_any(self, word):
        """ get the first phonological form for 'word' that you can find """

        for pos in self.lexemes['WTYPE']:
            if word in self.lexemes['WTYPE'][pos]:
                return self.lexemes['WTYPE'][pos][word], pos

        return None, None



# map MRC phonemes to their PatPho equivalents where they differ

# the MRC phonemes that need to be converted are:
# (the charachter between underscores roughly corresponds to the phoneme):

# 'e'  (p_e_t)
# '0'  (p_o_t)
# '9'  (pi_ng_)
# 'tS' (_ch_ain)
# 'dZ' (_j_eep)
# 'o'  (p_o_t) -- only uses

mrc_to_patpho_phonemes = {'e': 'E', '0': 'Q', '9': 'N', 'tS': 'C', 'dZ': 'J', 'o': 'Q'}


# additional chars in the DPHON field in the MRC database which need to be stripped from the phonological form
replace_with_empty_string = {'2', 'Q', '-', '+', 'R', "'"}


def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


def get_words_from_mrc(pathtodir):
    """ Function that goes through the MRC XLS file and extracts phonological representations """

    start_time = time.time()

    # map the MRC POS tags to more easily readable tags
    pos_conversion_dict = {'N': 'n', 'J': 'adj', 'V': 'v', 'A': 'adv', 'R': 'prep', 'C': 'conj', 'U': 'pron',
                           'I': 'interj', 'P': 'past_part', 'O': 'other'}

    # dictionary for mapping orthographic to phonological representations, organized by WTYPE vs. PDWTYOE and POS tag
    # WTYPE is a more fine-grained POS tag scheme; a word's PDWTYPE is its most common POS tag
    # if you want the phonology for a word's WTYPE but can't find it, you may want to go with its PDWTYPE instead
    mrc_dict = {'WTYPE':
                    {'n': {},  'adj': {},  'v': {},  'adv': {},  'prep': {},  'conj': {}, 'pron': {}, 'interj': {},
                     'past_part': {}, 'other': {}},

                'PDWTYPE':
                    {'v': {}, 'n': {}, 'adj': {}, 'other': {}}}


    print "Opening workbook"
    # get this from: http://www.psych.rl.ac.uk/Word_data.zip
    workbook = open_workbook(pathtodir + "/Word_data.xlsx")
    print "Workbook opened"

    for s in workbook.sheets():

        # go through the rows
        # if a sheet has less than 10 columns there's no need to go through it as the code below will fail.
        if s.ncols < 10:
            continue
        for row in range(s.nrows):

            try:
                # take the orthographic form from the 'WORD' field
                orthographic_form = str(s.cell(row, s.ncols - 4).value).lower()
                orthographic_form = orthographic_form.strip() # strip whitespace
                # take the POS tag from the 'WTYPE' field
                wtype = str(s.cell(row, s.ncols - 11).value)
                # take the phonological form from the DPHON field (not every word has an entry for the PHON field)
                phonemes = str(s.cell(row, s.ncols - 2).value)
                phonemes = phonemes.strip() # strip whitespace
                phonemes = ''.join([a if a not in replace_with_empty_string else '' for a in phonemes])
                phonemes = replace_all(phonemes, mrc_to_patpho_phonemes)
            # ignore Unicode problems -- this is very rare
            except UnicodeEncodeError:
                continue
            # continue if a word does not have an entry for the 'WORD', 'WTYPE, or 'PHON' field
            except IndexError:
                continue

            # skip the row if is orthographic word form, POS tag, or phoneme is the empty string
            if not (orthographic_form and wtype and phonemes):
                continue

            # sometimess the WTYPE of a word is erroneous, so check first before adding to 'mrc_dict'
            if wtype in pos_conversion_dict:
                mrc_dict['WTYPE'][pos_conversion_dict[wtype]][orthographic_form] = phonemes

            # if the word has an entry for 'PDWTYPE' (the most common POS tag for that word), get it
            # I think for each word there is probably only one entry with a PDWTYPE (the others are WTYPE only)
            try:
                pdwtype = str(s.cell(row, s.ncols - 10).value)
            except IndexError:
                continue
            except UnicodeEncodeError:
                continue

            if pdwtype in pos_conversion_dict:
                mrc_dict['PDWTYPE'][orthographic_form] = (phonemes, pos_conversion_dict[pdwtype])


    print "--- Done. This took %s minutes ---" % ((time.time() - start_time) / float(60))

    return MRCRepo(mrc_dict)


if __name__ == "__main__":

    mrc = get_words_from_mrc(os.getcwd())
    cPickle.dump(mrc, open(os.getcwd() + '/mrc.p', "wb"))