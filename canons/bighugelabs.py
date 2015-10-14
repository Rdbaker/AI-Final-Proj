"""
    Authors:
    Ryan Baker
    Matt Beaulieu
    Anthony Romeo
"""
from requests import get

URI = 'http://words.bighugelabs.com/api/2/917d8e3b5763c3881eb6171ddff17b47/{word}/json'


def canon(word):
    """Given a word, returns a list of synonyms in order of relevance"""
    r = get(URI.format(word=word))
    try:
        lists = r.json()
        matches = []
        if _has_verbs_and_nouns(lists):
            # alternate between adding a verb and a noun the the list
            while lists['verb']['syn'] or lists['noun']['syn']:
                if lists['verb']['syn']:
                    elt = lists['verb']['syn'][0]
                    matches.append(elt)
                    lists['verb']['syn'].remove(elt)
                if lists['noun']['syn']:
                    elt = lists['noun']['syn'][0]
                    matches.append(elt)
                    lists['noun']['syn'].remove(elt)
        elif _has_verbs(lists):
            matches = lists['verb']['syn']
        elif _has_nouns(lists):
            matches = lists['noun']['syn']
        return matches
    except:
        return []


def _has_verbs_and_nouns(lists):
    return _has_verbs(lists) and _has_nouns(lists)


def _has_verbs(lists):
    return lists.get('verb', False) and \
           lists['verb'].get('syn', False)


def _has_nouns(lists):
    return lists.get('noun', False) and \
           lists['noun'].get('syn', False)


if __name__ == "__main__":
    word = raw_input("What word are you looking up? ")
    canon(str(word))
