import os
import cPickle
import time
from xlrd import open_workbook

''' map MRC phonemes to their PatPho equivalents where they differ
the MRC phonemes that need to be converted are:
(the charachter between underscores roughly corresponds to the phoneme):

'e'  (p_e_t)
'0'  (p_o_t)
'9'  (pi_ng_)
'tS' (_ch_ain)
'dZ' (_j_eep)
'o'  (p_o_t) -- only uses'''
CONVERT = {'e': 'E', '0': 'Q', '9': 'N', 'tS': 'C', 'dZ': 'J', 'o': 'Q'}

# additional chars in the DPHON field in the MRC database which need to be stripped from the phonological form
REMOVE = {'2', 'Q', '-', '+', 'R', "'"}


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

    #dictionary for mapping orthographic to phonological representations, organized by WTYPE vs. PDWTYOE and POS tag
    #WTYPE is a more fine-grained POS tag scheme; a word's PDWTYPE is its most common POS tag
    #if you want the phonology for a word's WTYPE but can't find it, you may want to go with its PDWTYPE instead
    mrc_dict = {'WTYPE':
                    {'n': {},  'adj': {},  'v': {},  'adv': {},  'prep': {},  'conj': {}, 'pron': {}, 'interj': {},
                     'past_part': {}, 'other': {}},

                'PDWTYPE':
                    {'v': {}, 'n': {}, 'adj': {}, 'other': {}}}

    print "Opening workbook"
    # get this from: http://www.psych.rl.ac.uk/Word_data.zip
    workbook = open_workbook(pathtodir + "/Word_data.xlsx")
    print "Workbook opened"

    s = workbook.sheet_by_index(0)

    for row in range(s.nrows):

        # take the orthographic form from the 'WORD' field
        orthographic_form = unicode(s.cell(row, s.ncols - 4).value).lower()
        orthographic_form = orthographic_form.strip() # strip whitespace

        if not orthographic_form:
            continue

        # take the POS tag from the 'WTYPE' field
        wtype = unicode(s.cell(row, s.ncols - 11).value).strip()

        if not wtype:
            continue

        # take the phonological form from the DPHON field (not every word has an entry for the PHON field)
        phonemes = unicode(s.cell(row, s.ncols - 2).value)
        phonemes = ''.join([a for a in phonemes if a not in REMOVE])
        phonemes = replace_all(phonemes, CONVERT).strip()

        if not phonemes:
            continue

        # sometimess the WTYPE of a word is erroneous, so check first before adding to 'mrc_dict'
        try:
            mrc_dict['WTYPE'][pos_conversion_dict[wtype]][orthographic_form] = phonemes
        except KeyError:
            pass

        # if the word has an entry for 'PDWTYPE' (the most common POS tag for that word), get it
        pdwtype = unicode(s.cell(row, s.ncols - 10).value)

        try:
            mrc_dict['PDWTYPE'][orthographic_form] = (phonemes, pos_conversion_dict[pdwtype])
        except KeyError:
            continue

    print "--- Done. This took %s minutes ---" % ((time.time() - start_time) / float(60))

    return mrc_dict


if __name__ == "__main__":

    mrc = get_words_from_mrc(os.getcwd())
    cPickle.dump(mrc, open(os.getcwd() + '/mrc.p', "wb"))
