import os
import csv
import _pickle as cPickle
from pythonic_patpho import PatPho

pat_pho = PatPho()
try:
    filepath = os.path.join(os.getcwd(), 'mrc.p')
    mrc_dict = cPickle.load(open(filepath, 'rb'))
except FileNotFoundError as e:
    raise Exception("Could not find file: %s\nMake sure to run "
                    "'MRC_extract_phon_data.py first'" % filepath) from e

def mrc_words_to_csv(csv_path):
    """
    Go through every word in the MRC Psycholinguistic data base,
    use PyPatPho to create a phonological vector for each word,
    and write these to csv

    :param csv_path:    path to CSV file with phonological vector
                        (to be created)
    """
    with open(csv_path, 'w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_ALL)
        first_row = ['part_of_speech', 'word', 'binary_vector', 'real_vector']
        writer.writerow(first_row)

        n_words = 0
        for pos_tag in mrc_dict['WTYPE'].keys():
            for word in mrc_dict['WTYPE'][pos_tag]:
                phonemes = mrc_dict['WTYPE'][pos_tag][word]
                try:
                    binary_v = pat_pho.get_phon_vector(phonemes, binary=True)
                    float_v = pat_pho.get_phon_vector(phonemes, binary=False)
                except TypeError: # word is too long, or unknown phoneme
                    continue
                binary_v = ','.join(str(i) for i in binary_v)
                float_v = ','.join(str(i) for i in float_v)
                writer.writerow([pos_tag, word, binary_v, float_v])
                n_words += 1

        print('Created phonological representations for %s words' % n_words)


if __name__ == '__main__':

    fp = os.path.join(os.getcwd(), 'mrc_words.csv')
    mrc_words_to_csv(fp)