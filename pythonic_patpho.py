class PatPho(object):

    """
    Attempt at a Pythonic re-write of PatPho.

    Only supports left-justified format right now.
    """

    def __init__(self):

        self.syllabic_grid = None
        self. idx = None
        self.init_syllabic_grid_and_index()

        self.vowels = {"i", "I", "e", "E", "&", "@", "3", "V", "a", "U", "u", "O", "A", "Q"}

        self.phonemes = {"i": [0, 1, 0, 1, 1], "I": [0, 1, 0, 0, 1], "e": [0, 1, 1, 0, 1], "E": [0, 1, 1, 1, 0],
                         "&": [0, 1, 1, 0, 0], "@": [1, 1, 1, 0, 0], "3": [1, 1, 0, 0, 1], "V": [1, 1, 1, 1, 0],
                         "a": [1, 1, 1, 0, 0], "U": [1, 0, 0, 1, 1], "u": [1, 0, 0, 0, 1], "O": [1, 0, 1, 0, 1],
                         "A": [1, 0, 1, 0, 0], "Q": [1, 0, 1, 1, 0], 'VO': [0, 0, 0, 0, 0],
                         "p": [0, 0, 0, 0, 0, 1, 0], "t": [0, 0, 1, 1, 0, 1, 0], "k": [0, 1, 1, 0, 0, 1, 0],
                         "b": [1, 0, 0, 0, 0, 1, 0], "d": [1, 0, 1, 1, 0, 1, 0], "g": [1, 1, 1, 0, 0, 1, 0],
                         "m": [1, 0, 0, 0, 0, 0, 1], "n": [1, 0, 1, 1, 0, 0, 1], "N": [1, 1, 1, 0, 0, 0, 1],
                         "l": [1, 0, 1, 1, 0, 1, 1], "r": [1, 0, 1, 1, 1, 1, 0], "f": [0, 0, 0, 1, 1, 0, 0],
                         "v": [1, 0, 0, 1, 1, 0, 0], "s": [0, 0, 1, 1, 1, 0, 0], "z": [1, 0, 1, 1, 1, 0, 0],
                         "S": [0, 1, 0, 0, 1, 0, 0], "Z": [1, 1, 0, 0, 1, 0, 0], "j": [1, 1, 0, 1, 0, 1, 1],
                         "h": [0, 1, 1, 1, 0, 1, 1], "w": [1, 1, 1, 0, 0, 1, 1], "T": [0, 0, 1, 0, 1, 0, 0],
                         "D": [1, 0, 1, 0, 1, 0, 0], "C": [0, 1, 0, 1, 1, 0, 0], "J": [1, 1, 0, 1, 1, 0, 0],
                         'CO': [0, 0, 0, 0, 0, 0, 0]}


    def init_syllabic_grid_and_index(self):
        self.idx = 0
        self.syllabic_grid = ['CO', 'CO', 'CO', 'VO', 'VO', 'CO', 'CO', 'CO', 'VO', 'VO', 'CO', 'CO', 'CO', 'VO', 'VO',
                              'CO', 'CO', 'CO']


    def index_to_next_vowel(self):
        for i in self.syllabic_grid[self.idx:]:
            if i == 'VO':
                break
            self.idx += 1


    def index_to_next_consonant(self):
        for i in self.syllabic_grid[self.idx:]:
            if i == 'CO':
                break
            self.idx += 1


    def insert_phoneme_into_grid(self, phoneme):

        if phoneme in self.vowels:
            self.index_to_next_vowel()
            self.syllabic_grid[self.idx] = phoneme

        elif phoneme in self.phonemes:
            self.index_to_next_consonant()
            self.syllabic_grid[self.idx] = phoneme

        else:
            raise Exception('Unknown phoneme: %s' % phoneme)


    def get_phon_vector(self, phonemes):

        # go through the phonemes and insert them into the metrical grid
        for p in phonemes:
            self.insert_phoneme_into_grid(p)

        # convert metrical grid to vector
        phon_vector = []
        for i in self.syllabic_grid:
            phon_vector.extend(self.phonemes[i])

        # reset metrical grid
        self.init_syllabic_grid_and_index()

        return phon_vector




if __name__ == "__main__":


    pat_pho = PatPho()


    # some test cases, phonological represntations taken from MRC

    print pat_pho.get_phon_vector('@Uld') # adejctive 'old'

    print pat_pho.get_phon_vector('weIt') # verb 'wait'

    print pat_pho.get_phon_vector('hI@') # verb 'hear'