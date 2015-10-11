# Matthew Beaulieu, Anthony Romeo, Ryan Baker
# Synonym Finder takes in some synonym, and returns a word the user
# is thinking of

# Thesaurus is a wrapper class for a thesaurus
# word_list returns a list of words that're a synonym for the given word
# get_multiplier returns the multiplier of the thesaurus given how good
# it has been thus far

from __future__ import division

from canons.thesaurus import THESAURI
# from canons.utils import OrderedSet


def synonym_finder(wrd):
    """Find synonyms from a word"""
    master_list = []
    # thesaurus_total = sum([thes.value for thes in THESAURI])
    for i, t in enumerate(THESAURI):
        syn_list = t.find_syns(wrd)
        for idx, word in enumerate(syn_list):
            flag = 0
            # multiplier = (Thesaurus.get_multiplier/ thesaurus_total) *
            multiplier = (len(syn_list) - idx) / len(syn_list)
            for m_idx, item in enumerate(master_list):
                if item['word'] == word:
                    master_list[m_idx]['value'] += multiplier
                    master_list[m_idx]['thes_idxs'] += [i]
                    flag = 1
            if flag == 0:
                master_list.append({'word': word,
                                    'value': multiplier,
                                    'thes_idxs': [i]})

    master_list.sort(key=lambda d: -d['value'])
    print filter(lambda word: edit_distance(wrd, word['word']) > 2, master_list)[:5]
    return filter(lambda word: edit_distance(wrd, word['word']) > 2, master_list)[:5]


# Edit distance function taken from:
# http://stackoverflow.com/questions/2460177/edit-distance-in-python
def edit_distance(wrd1, wrd2):
    len_1 = len(wrd1)
    len_2 = len(wrd2)

    # the matrix whose last element ->edit distance
    x = [[0]*(len_2+1) for _ in range(len_1+1)]

    for i in range(0, len_1+1): #initialization of base case values
        x[i][0]=i

    for j in range(0,len_2+1):
        x[0][j]=j

    for i in range (1,len_1+1):
         for j in range(1,len_2+1):
             if wrd1[i-1]==wrd2[j-1]:
                 x[i][j] = x[i-1][j-1]
             else:
                 x[i][j]= min(x[i][j-1],x[i-1][j],x[i-1][j-1])+1

    return x[i][j]

if __name__ == '__main__':
    word = raw_input("What is a synonym of the word you're looking for? ")
    synonym_finder(str(word))
