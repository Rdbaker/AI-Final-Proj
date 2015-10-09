"""
    Authors:
    Ryan Baker
    Matt Beaulieu
    Anthony Romeo
"""
from requests import get

URI = 'http://watson.kmi.open.ac.uk/API/term/synonyms?term={word}'


def canon(word):
    """Given a word, returns a list of synonyms in order of relevance"""
    r = get(URI.format(word=word), headers={'Accept': 'application/json'})
    print r.json()
    print dir(r)


if __name__ == "__main__":
    word = raw_input("What word are you looking up? ")
    canon(str(word))
