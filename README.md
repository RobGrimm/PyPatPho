# PyPatPho

A phonological pattern generator. Input phonological forms using the [CELEX]() database phoneme inventory, and PyPatPho will convert this to either a binary or real-valued vector representation, which can then be used as input to, for example, machine learning algorithms. This code is based on the [PatPho Paper](http://blclab.org/wp-content/uploads/2013/02/patpho.pdf) by [Li](http://blclab.org/ping-li/) and [Macwhinney](http://psyling.psy.cmu.edu/).

Because the word vectors are created in a similar way, similar-sounding things will be in the same place in the vector space, which is illustrated by the figure below. As seen in this figure, words that rhyme are tightly clustered together, which illustrates that they have a high degree of similarity.

![bh-sne visualization of phonological vector space](/rhymes.png?raw=true "bh-sne visualization of vector space")

# Version

1.1

# Requirements

Python 3.X. Can reasonably be expected to work on all platforms that can run Python.

# Usage

Simply download the PyPatPho code and put it somewhere. The main file to import is 'pythonic_patpho.py'.

```python
from pythonic_patpho import PatPho

patpho = PatPho(binary=True) 						# create patpho object 
old = patpho.get_phon_vector('@Uld', left=True)   	# get phoneme vector representation of the word 'old'

print old # output: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

```

If you don't have access to CELEX, you can use the [MRC database](http://ota.oucs.ox.ac.uk/headers/1054.xml). 

We provide a script ('MRC_extract_phon_data.py') that automatically converts the MRC phonemic representations to the CELEX phoneme inventory. The script relies on an XLS file containing the MRC database that used to be available [here](http://www.psych.rl.ac.uk/Word_data.zip). Since the link no longer works, we provide the XLS file ('PyPatPho/Word_data.xls') as is. The 'MRC_extract_phon_data.py' script will open the 'Word_data.xls' file and create a pickled dictionary for further use -- see the 'visualize_examples.py' script for an example of how it should be used together with the PatPho class. 

You can also create a csv file with phonological vectors for all words contained in the MRC database. To do this, first run 'MRC_extract_phon_data.py', followed by 'create_csv_with_MRC_words.py'. This will create a csv file with columns 'part_of_speech', 'word', 'binary_vector', and 'real_vector'. 

# Contributors

Robert Grimm   
Stéphan Tulkens
