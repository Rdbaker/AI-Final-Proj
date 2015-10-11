# Matthew Beaulieu, Anthony Romeo, Ryan Baker
# Synonym Finder takes in some synonym, and returns a word the user
# is thinking of

# Thesaurus is a wrapper class for a thesaurus
# word_list returns a list of words that're a synonym for the given word
# get_multiplier returns the multiplier of the thesaurus given how good it has been thus far

from __future__ import division

from canons.thesaurus import THESAURI
from canons.utils import thesaurus

def synonym_finder(wrd):
    master_list = []
    for thes in THESAURI:
        thes.read_logs("")
  	thesaurus_total = thes.value
        temp_list = thes.find_syns(wrd)
	words_list.append(thesaurus.find_syns(wrd))
        
        for word in temp_list:
            flag = 0
            #multiplier = (Thesaurus.get_multiplier/ thesaurus_total) * 
            multiplier = (len(temp_list) - temp_list.index(word)) / len(temp_list)
            for item  in master_list:
                if item[0] == word:
                    multiplier2 = master_list[master_list.index(item)][1]
                    thes_list.master_list[master_list.index(item)][1]
                    master_list[master_list.index(item)] = (word, (multiplier + multiplier2))
                    flag = 1
            if flag == 0:
                master_list.append((word, multiplier))
    
    master_list.sort(key=lambda tup: tup[1])
    print master_list

    return_list = []
    for word in master_list:
        if (edit_distance(wrd, word) > 2):
            return_list.append(word[0])
        if len(return_list) == 5:
            return return_list
    return return_list

# Edit distance function taken from:
# http://stackoverflow.com/questions/2460177/edit-distance-in-python
def edit_distance(wrd1, wrd2):
    len_1=len(wrd1)
    len_2=len(wrd2)

    x =[[0]*(len_2+1) for _ in range(len_1+1)]#the matrix whose last element ->edit distance

    for i in range(0,len_1+1): #initialization of base case values
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
    synonym_finder("happy")
