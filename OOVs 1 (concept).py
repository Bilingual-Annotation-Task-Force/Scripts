"""
Eric Nordstrom
3/5/17
Python 3.6.0

Concept for removing OOV tokens from token list
"""

D1 = {"hi","hello","see ya","goodbye"} #English dictionary
D2 = {"oye","hola","hasta luego","adios"} #Spanish dictionary

OOVs = {} #tokens not found in either dictionary to be added here
tokens = ['hi','hola',"'sup",'adios']

d = 0 #for adjusting count in "for" loop

for i in range(0,len(tokens)):

    n = i - d #adjusted to account for missing OOV words
    word = tokens[n]

    if(word in D1 or word in D2):
        action = "Found."

    else:
        action = "Not found. Removed from TOKENS list."
        OOVs.update({i:word}) #i is the original index of WORD in TOKENS (not necessarily the current index as words may have been deleted before this one)
        del tokens[n]
        d += 1

    print(str(i) + ': "' + word + '". ' + action)

print('\nRemaining tokens:')
print(tokens)
print('OOVs removed:')
print(OOVs)
