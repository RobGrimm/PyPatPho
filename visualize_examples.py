import os
import _pickle as cPickle
from pythonic_patpho import PatPho


# list of 100 commons nouns from: http://stickyball.net/esl-grammar-worksheets.html?id=85
nouns = ['letter', 'number', 'person', 'pen', 'class', 'people', 'sound', 'water', 'side', 'place', 'man',
         'men', 'woman', 'women', 'boy', 'girl', 'year', 'day', 'week', 'month', 'name', 'sentence', 'line',
         'air', 'land', 'home', 'hand', 'house', 'picture', 'animal', 'mother', 'father', 'brother', 'sister',
         'world', 'head', 'page', 'country', 'question', 'answer', 'school', 'plant', 'food', 'sun', 'state',
         'eye', 'city', 'tree', 'farm', 'story', 'sea', 'night', 'day', 'life', 'north', 'south', 'east', 'west',
         'child', 'children', 'example', 'paper', 'music', 'river', 'car', 'foot', 'feet', 'book', 'science',
         'room', 'friend', 'idea', 'fish', 'mountain', 'horse', 'watch', 'colour', 'face', 'wood', 'list',
         'bird', 'body', 'dog', 'family', 'song', 'door', 'product', 'wind', 'ship', 'area', 'rock', 'order',
         'fire', 'problem', 'piece', 'top', 'bottom', 'king', 'space']

# list of one-syllable rhymes from: http://www.rhymer.com/RhymingDictionary/list.html?ref=binfind.com/web
rhymes1 = ['cyst', 'fist', 'gist', 'grist', 'hissed', 'kissed', 'list', 'missed', 'mist', 'tryst',
           'twist',	'whist', 'wrist', 'assist']

# list of two-syllable rhymes from: http://www.rhymer.com/RhymingDictionary/list.html?ref=binfind.com/web
rhymes2 = ['baptist', 'blacklist', 'consist', 'desist', 'dismissed', 'enlist', 'exist', 'insist', 'persist', 'resist',
           'subsist', 'untwist']


pat_pho = PatPho()
mrc_dict = cPickle.load(open(os.getcwd() + '/mrc.p', 'rb'))


vectors = dict()

for word in nouns + rhymes1 + rhymes2:

    try:
         phonemes = mrc_dict['WTYPE']['n'][word]
    except KeyError:
        phonemes = mrc_dict['WTYPE']['v'][word]

    vectors[word] = pat_pho.get_phon_vector(phonemes)








