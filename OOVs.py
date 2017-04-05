"""
Eric Nordstrom
Python 3.6.0
3/31/2017

Version 2
Improvement on concept for removing out-of-vocabulary (OOV) words (AKA "mixed words") from tokens list
Uses .txt file with user prompts for Spanish dictionary
"""

import os
os.chdir(input("Please provide working directory: ")) #This line should be modified if changing the working directory is not desired.

'''Get dictionaries'''
D1 = {"hi","hello","see ya","goodbye"} #English dictionary placeholder
D2name = input("Please provide name of .txt file for Spanish dictionary: ")
D2encoding = input("Please provide encoding type for Spanish dictionary: ") #Different .txt files use different encoding for reading characters.
if D2name[-4:] != ".txt":
    D2name += ".txt" #adds ".txt" suffix if not already present
D2 = open(D2name,encoding=D2encoding).read().split() #Spanish dictionary. Class of D2 will be LIST.

'''Get tokens list'''
tokens = ['hi','hola',"'sup",'adios'] #tokens list placeholder

'''Initialize'''
OOVs = {} #tokens not found in either dictionary to be added here
d = 0 #for adjusting count in "for" loop after OOV removals

'''Find OOVs'''
for i in range(0,len(tokens)):

    n = i - d #adjusted with d to account for missing OOV words
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
