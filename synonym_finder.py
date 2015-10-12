# Matthew Beaulieu, Anthony Romeo, Ryan Baker
# Synonym Finder takes in some synonym, and returns a word the user
# is thinking of

# Thesaurus is a wrapper class for a thesaurus
# word_list returns a list of words that're a synonym for the given word
# get_multiplier returns the multiplier of the thesaurus given how good
# it has been thus far

from __future__ import division

from canons.thesaurus import THESAURI


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
                if item['word'].lower() == word.lower():
                    master_list[m_idx]['value'] += multiplier + t.value
                    master_list[m_idx]['thes_meta'].append({
                            'thesaurus': t,
                            'thesaurus_word_value': multiplier})
                    flag = 1
            if flag == 0:
                master_list.append({'word': word,
                                    'value': multiplier + t.value,
                                    'thes_meta': [{
                                        'thesaurus': t,
                                        'thesaurus_word_value': multiplier}]})

    master_list.sort(key=lambda d: -d['value'])
    return filter(lambda word: edit_distance(wrd, word['word']) > 2,
                  master_list)[:10]


# Edit distance function taken from:
# http://stackoverflow.com/questions/2460177/edit-distance-in-python
def edit_distance(wrd1, wrd2):
    len_1 = len(wrd1)
    len_2 = len(wrd2)
    # the matrix whose last element ->edit distance
    x = [[0]*(len_2+1) for _ in range(len_1+1)]
    # initialization of base case values
    for i in range(0, len_1+1):
        x[i][0] = i
    for j in range(0, len_2 + 1):
        x[0][j] = j
    for i in range(1, len_1+1):
        for j in range(1, len_2+1):
            if wrd1[i-1] == wrd2[j-1]:
                x[i][j] = x[i-1][j-1]
            else:
                x[i][j] = min(x[i][j-1], x[i-1][j], x[i-1][j-1])+1
    return x[i][j]


def log_zeros(input_word):
    for thes in THESAURI:
        thes.add_score(input_word, '', 0)


def log_records(choice, syns, input_word):
    for thes in THESAURI:
        found = False
        for entry in syns[choice]['thes_meta']:
            if entry['thesaurus'] == thes:
                thes.add_score(input_word,
                               syns[choice]['word'],
                               entry['thesaurus_word_value'])
                found = True
                break
        if not found:
            thes.add_score(input_word, syns[choice]['word'], 0)

if __name__ == '__main__':
    word = raw_input("What is a synonym of the word you're looking for? ")
    syns = synonym_finder(str(word))
    print [(i, str(syn['word'])) for i, syn in enumerate(syns)]
    choice = raw_input("Which of these words is the closest to the word you " +
                       "were looking for (zero indexed)? (press enter if none) ")
    try:
        if choice == '':
            log_zeros(word)
        else:
            log_records(int(choice), syns, word)
    except:
        exit(1)
