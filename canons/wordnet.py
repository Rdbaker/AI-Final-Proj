"""
    Authors:
    Ryan Baker
    Matt Beaulieu
    Anthony Romeo
"""
from nltk.corpus import wordnet as wn
from utils import OrderedSet


def canon(word):
    """Given a word, returns a list of synonyms in order of relevance"""
    # this is kind of fragile, maybe do something better about this
    return OrderedSet([syn.unicode_repr().split("'")[1].split('.')[0] for syn in wn.synsets(word)])


if __name__ == "__main__":
    word = raw_input("What word are you looking up? ")
    canon(str(word))
