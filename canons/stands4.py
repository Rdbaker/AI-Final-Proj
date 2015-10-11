"""
    Authors:
    Ryan Baker
    Matt Beaulieu
    Anthony Romeo
"""
from requests import get
from bs4 import BeautifulSoup

URI = 'http://www.stands4.com/services/v2/syno.php?uid=4412&tokenid=92XGfHe4TOMhvfEv&word={word}'


def canon(word):
    """Given a word, returns a list of synonyms in order of relevance"""
    soup = BeautifulSoup(get(URI.format(word=word)).content, 'xml')
    syns = []
    syn_lists = [child.text.split(', ') for child in soup.results('synonyms')]
    while any(syn_lists):
        for lst in syn_lists:
            if lst:
                syns.append(lst[0])
                lst.remove(lst[0])
    return filter(lambda word: len(word) > 0, syns)


if __name__ == "__main__":
    word = raw_input("What word are you looking up? ")
    canon(str(word))
