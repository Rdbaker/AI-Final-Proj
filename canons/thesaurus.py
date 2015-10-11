"""
    Authors:
    Ryan Baker
    Matt Beaulieu
    Anthony Romeo
"""
from canons import altervista
from canons import bighugelabs
from canons import stands4
from canons import watson
from canons import wordnet
from canons.utils import Thesaurus

THESAURI = [
    Thesaurus(altervista.canon, 'canons/logs/altervista.json'),
    Thesaurus(bighugelabs.canon, 'canons/logs/bighugelabs.json'),
    Thesaurus(stands4.canon, 'canons/logs/stands4.json'),
    Thesaurus(watson.canon, 'canons/logs/watson.json'),
    Thesaurus(wordnet.canon, 'canons/logs/wordnet.json')
    ]


THESAURUSES = THESAURI
