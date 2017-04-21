"""

Eric Nordstrom
Python 3.6.0
4/12/17



Version 3
First usable version

Defines OOV_remove method, which takes an input of a LIST (tokens) and two language
"dictionaries" of unspecified type (SET recommended) and outputs a TUPLE containing:
    (1) the same tokens LIST with out-of-vocabulary (OOV) words (a.k.a. "mixed
        words") removed and
    (2) a DICT hashed with indices denoting the original position of the
        corresponding OOV word in the tokens LIST.
If only one "dictionary" is provided, the second will be from the PyDictionary
module by default. Using PyDictionary requires downloading the PyDictionary module;
PyDictionary requires a reliable internet connection.

Gettxt method can be used for retrieving words from .txt files as LISTs. To change
to SET type, use set(___) function.

PyDict method called in OOV_remove method for case of PyDictionary option.

TOKENS arguments must be properly tokenized beforehand. SPLIT() only splits based on
whitespace.



Example code:
    
    import os
    os.chdir( Preferred_Working_Directory )
    from OOVs import OOV_remove, gettxt
    
    tokens = gettxt( "Tokens Text File", "utf8" ) #LIST type
    SpnDict = set( gettxt( "Spanish Dictionary.txt", "utf8" ) ) #SET type
    '''No English dictionary specified --> will use PyDictionary'''

    ( tokens_without_OOVs, OOV_words ) = OOV_remove( tokens, SpnDict )
    number_of_OOVs = len( OOV_words )

"""


def PyDict(): #for default D2 argument in OOV_remove
    from PyDictionary import PyDictionary
    return PyDictionary()


def OOV_remove(tokens,D1,D2=PyDict()):

    if type(D2) in {set,list,tuple,dict}:
        def condition(word,D1,D2): #condition for IF statement in FOR loop
            return not(word in D1 or word in D2)
        
    else: #assume PyDictionary

        import sys, os
        s = sys.stdout #to save for later
        sys.stdout = open(os.devnull,'w') #prevents printing to console during PyDictionary usage
        
        def condition(word,D1,D2):
            return word not in D1 and D2.meaning(word) == None #This line would print to the console on each OOV if the STDOUT were not changed.

    t = list(tokens) #to become output tokens LIST with OOVs removed
    OOVs = {} #to become DICT containing removed OOVs hashed with their original indices in TOKENS
    d = 0 #index offset to account for already removed OOV words

    for i in range(0,len(tokens)):
        
        word = tokens[i]
        
        if condition(word,D1,D2):
            OOVs.update({i:word})
            del t[i-d]
            d += 1

    if type(D2) not in {set,list,tuple,dict}: #i.e. PyDictionary
        sys.stdout = s #return printing to original settings
    
    return (t,OOVs)


def gettxt(file_name,encoding_type):

    name = file_name

    if name[-4:] != '.txt':
        name += '.txt'

    return open(name,encoding=encoding_type).read().split() #LIST type
