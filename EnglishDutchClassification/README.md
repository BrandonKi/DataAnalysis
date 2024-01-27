## English/Dutch Language Classification

The model will classify whether a data sample is in English or Dutch given 15 words. A dictionary for each respective langauge was not used(that would be cheating!). A full list of features are in the `extract_features()` function in the `common.py` file.

I implemented two models(no libraries), one being a [decision tree](https://en.wikipedia.org/wiki/Decision_tree#:~:text=A%20decision%20tree%20is%20a,only%20contains%20conditional%20control%20statements.) and the other being [AdaBoost](https://en.wikipedia.org/wiki/AdaBoost).


Trained on wikipedia articles. See `generate_data.py` for details.

## Documentation

The general command line argument format is the following:

### train \<examples\> \<hypothesisOut\> \<learning-type\>

* examples is a file containing labeled examples

* hypothesisOut specifies the file name to write your model to

* learning-type specifies the type of learning algorithm you will run, it is either "dt" or "ada"

### predict \<hypothesis\> \<file\>
* hypothesis is a trained decision tree or ensemble created by the train program

* file is a file containing lines of 15 word sentence fragments in either English or Dutch


### There are a few datasets provided:
* small_train.dat

small_train.dat is a small dataset with 20 of each classification.

* large_train.dat

large_train.dat is a much bigger dataset with an unbalanced amount of classifications.
There are 4717 entries in the dataset.


* test_set.dat

test_set.dat is a labelled dataset with data points not seen in either training set and is used to give an estimate of how good the model is while training.

* test.dat

test.dat is unlabelled data and is used as a true test to see how well the model can predict


### To train a dt model run the following:

    python3 train.py data/small_train.dat models/out.model dt

### To use that model for predicting run the following:

    python3 predict.py models/out.model data/test.dat

### To train an ada model instead you would run:

    python3 train.py data/small_train.dat models/out.model ada