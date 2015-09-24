# PyPatPho

A phonological pattern generator. Input phonological forms using the [CELEX]() database phoneme inventory, and PyPatPho will convert this to either a binary or real-valued vector representation, which can then be used as input to, for example, machine learning algorithms. This code is based on the [PatPho Paper](http://blclab.org/wp-content/uploads/2013/02/patpho.pdf) by [Li](http://blclab.org/ping-li/) and [Macwhinney](http://psyling.psy.cmu.edu/).

Because the word vectors are created in a similar way, similar-sounding things will be in the same place in the vector space, which is illustrated by the figure below. As seen in this figure, words that rhyme are tightly clustered together, which illustrates that they have a high degree of similarity.

![bh-sne visualization of phonological vector space](/rhymes.png?raw=true "bh-sne visualization of vector space")

# Version

1.0

# Requirements

Python 2.X. Tested on mac OSX and Ubuntu using Python 2.7. Can reasonably be expected to work on all platforms that can run Python.

# Usage

Simply download the PyPatPho code and put it somewhere. The main file to import is 'pythonic_patpho.py'.

```python
from pythonic_patpho import PatPho

patpho = PatPho(binary=True) 						# create patpho object 
old = patpho.get_phon_vector('@Uld', left=True)   	# get phoneme vector representation of the word 'old'

print old # output: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

```

If you don't have access to CELEX, you can use the MRC database, which is free to download [here](http://ota.oucs.ox.ac.uk/headers/1054.xml). The 'MRC_extract_phon_data.py' script will open the Word_data.xls file found on this page and automatically converts the phonemic representations to the CELEX phoneme inventory. It will create a pickled dictionary for further use -- see the 'visualize_examples.py' script for an example of how it should be used together with the PatPho class. 

# Contributors

Robert Grimm   
Stéphan Tulkens
