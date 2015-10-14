"""
    Authors:
    Ryan Baker
    Matt Beaulieu
    Anthony Romeo
"""
from requests import get
from utils import OrderedSet

URI = 'http://thesaurus.altervista.org/thesaurus/v1?key=9nGRHa5KIPomoDa2GzbO&word={word}&language=en_US&output=json'


def canon(word):
    """Given a word, returns a list of synonyms in order of relevance"""
    url = URI.format(word=word)
    r = get(url)
    try:
        # get the word lists from the response
        word_lists = [lst['list']['synonyms'].split('|') for lst in r.json()['response']]
        # concatenate the word lists and eliminate duplicates
        return list(OrderedSet([item for sublist in word_lists for item in sublist if '(antonym)' not in item]))
    except:
        return []

if __name__ == "__main__":
    word = raw_input("What word are you looking up? ")
    canon(str(word))
