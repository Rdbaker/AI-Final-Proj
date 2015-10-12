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
    Thesaurus(altervista.canon, 'canons/viz/logs/altervista.json'),
    Thesaurus(bighugelabs.canon, 'canons/viz/logs/bighugelabs.json'),
    Thesaurus(stands4.canon, 'canons/viz/logs/stands4.json'),
    Thesaurus(watson.canon, 'canons/viz/logs/watson.json'),
    Thesaurus(wordnet.canon, 'canons/viz/logs/wordnet.json')
    ]


THESAURUSES = THESAURI
