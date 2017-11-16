"""
Eric Nordstrom
Python 3.6.0
November 15 2017

Incomplete.
"""


#Classes for holding data

class affgroup:
    '''Precursor to prefgroup and suffgroup classes; not for standalone use.'''
    def __init__( self, **kwargs ):
        self.order = 1
        self.orthographic = self.lexicon = {}
        if 'order' in kwargs:
            if kwargs['order'] < 1:
                raise ValueError( 'Order of zero reserved for stem types.' )
            self.order = kwargs['order']
        if 'lexicon' in kwargs:
            self.lexicon = kwargs['lexicon'] #dict with key = name and contents = tuple containing: (1) the default form and (2) a subdict. in the subdict: key = regular expression or tuple of regular expressions; contents = alternate form of affix
        if 'orthographic' in kwargs:
            self.orthographic = kwargs['orthographic'] #dict with key = regular expression or tuple of regular expressions and contents = tuple or set of tuples with (1) integer indicating index or string indicating range of characters to replace (e.g. '-1', '3:5', or ':') and (2) string to replace them. In key, can additionally include True or False to for AND argument.
    def __str__( self ):
        return 'affix group ' + str( self.order )

#lexicon example:
#   { 'PL' : ( 's', { '.*[oysz]' : 'es', 'person' : '', '.*u[sm]' : '' } ), ... }
#   This is a lexicon entry with a set of orthographic rules for changing the affix based on the stem.
#   This should be applied before orthographic changes to the stem.
#
#orthographic example:
#   { '.*y' : (-1, 'i'), '.*person' : (':', 'people'), '.*us' : ('-2:', 'i'), '.*um' : ('-2:', 'a') }
#   This is a set of orthographic rules for changing the stem based on itself and the affix in question.

class prefgroup( affgroup ):
    '''Data for a group of prefixes sharing the same order of application, orthographic changes to the stem, and rules for preceding other morpheme groups'''
    def __init__( self, **kwargs ):
        affgroup.__init__( self, **kwargs )
        self.can = False #whether specifying "can_" or "cannot_" + "precede"
        if 'can_precede' in kwargs:
            self.can = True
            self.precede = set( kwargs['can_precede'] )
        if 'cannot_precede' in kwargs:
            self.precede = set( kwargs['cannot_precede'] )

class suffgroup( affgroup ):
    '''Data for a group of suffixes sharing the same order of application, orthographic changes to the stem, and rules for following other morpheme groups'''
    def __init__( self, **kwargs ):
        affgroup.__init__( self, **kwargs )
        self.can = False #whether specifying "can_" or "cannot_" + "follow"
        if 'can_follow' in kwargs:
            self.can = True
            self.follow = set( kwargs['can_follow'] )
        elif 'cannot_follow' in kwargs:
            self.follow = set( kwargs['cannot_follow'] )
        else:
            self.follow = set()


#Classes for representing and processing text as morphemes

class morpheme:
    '''Precursor to root and affix classes; not for standalone use.'''
    def __init__( self, name='', groupname='' ):
        self.name = name #e.g. "1SG" for an affix or "bird" for a stem
        self.groupname = groupname #name of stem or affix group. note: affgroup objects don't have names; the name is just a lookup in AFFS.

class root( morpheme ):
    def __init__( self, name='', groupname='' ):
        morpheme.__init__( self, name, groupname )
        self.order = 0
    def __repr__( self ):
        return self.name + '+' + self.groupname #e.g. "bird+N"
    def __str__( self ):
        return self.name

class affix( morpheme ):
    def __init__( self, name='', groupname='' ):
        morpheme.__init__( self, name, groupname )
        self.order = AFFS[self.groupname].order
        self.afftype = type( AFFS[self.groupname] ) #prefgroup or suffgroup
    def __repr__( self ):
        return  self.name
    def __str__( self ):
        return AFFS[self.groupname].lexicon[self.name][0]
    def mod( self, wordpart ):
        '''Modify the affix and/or stem according to orthographic rules.'''
        aff = str( self )
        rules = AFFS[self.groupname].lexicon[self.name][1]
        #orthographic changes to affix
        for rule in rules:
            if rulematch( wordpart, rule ):
                aff = rules[rule]
                break
        #orthographic changes to rest of word
        rules = AFFS[self.groupname].orthographic
        for rule in rules:
            if rulematch( wordpart, rule ):
                changes = rules[rule]
                if type( changes ) == tuple:
                    changes = { changes }
                changeinfo = []
                for change in changes:
                    ind = change[0]
                    text = change[1]
                    if type( ind ) == int:
                        ind1 = ind
                        ind2 = ind + 1
                    else:
                        colonloc = ind.find(':')
                        ind1 = ind[:colonloc]
                        ind2 = ind[colonloc+1:]
                        if ind1 == '':
                            ind1 = 0
                        else:
                            ind1 = int( ind1 )
                        if ind2 == '':
                            ind2 = len( wordpart )
                        else:
                            ind2 = int( ind2 )
                    if ind2 == 0 and ind1 < 1: #correction for weird property of python indices (IMO)
                        ind2 = len( wordpart )
                    changeinfo += [ (ind1, ind2, text) ]
                changeinfo.sort()
                newtext = ''
                prevend = 0
                for ind1, ind2, text in changeinfo:
                    newtext += wordpart[prevend:ind1] + text
                    prevend = ind2
                newtext += wordpart[prevend:]
                wordpart = newtext
                break
        if self.afftype == prefgroup:
            return aff + wordpart
        else:
            return wordpart + aff

class morphemes:
    def __init__( self, morphs=[] ):
        self.morphs = list( morphs )
        self.root = [ morph for morph in morphs if type( morph ) == root ][0]
        self.rootindex = morphs.index( self.root )
    def order( self ):
        O = []
        for morph in self.morphs:
            O += [ morph.order ]
        return O
    def __repr__( self ):
        parserep = ''
        for morph in self.morphs:
            parserep += repr( morph ) + '+'
        return parserep[:-1]
    def __str__( self ):
        word = str( self.root )
        L = len( self.morphs )
        prefindex = self.rootindex - 1
        suffindex = self.rootindex + 1
        pref_remaining = prefindex >= 0
        suff_remaining = suffindex < L
        while pref_remaining or suff_remaining:
            if pref_remaining:
                prefix = self.morphs[prefindex]
            else:
                prefwin = False
            if suff_remaining:
                suffix = self.morphs[suffindex]
                if pref_remaining:
                    if prefix.order <= suffix.order:
                        prefwin = True
                    else:
                        prefwin = False
            else:
                prefwin = True
            if prefwin:
                word = prefix.mod( word )
                prefindex -= 1
                pref_remaining = prefindex >= 0
            else:
                word = suffix.mod( word )
                suffindex += 1
                suff_remaining = suffindex < L
        return word


#Functions

##def morphoparse( word, *affixes, **stems, err_res=True ):
##    '''Returns a possible parsing of the given word into the morphemes it consists of.
##AFFS: dicts for each affix type. "name" for name, "order" for order in which to apply rules (default: lowest positive integer not yet taken), "can follow" for list of morpheme types it can follow, "can precede"/"cannot precede"/"can follow"/"cannot follow" for list(s) of allowed/prohibited adjacent morpheme types, "ortho" for list of orthographic rules as condition list-output pairs (e.g. "=='goose'" or ".endswith('y')").
##STEMS: lists of stems of each group (e.g. noun=['aardvark', ...], verb=[..., ...], ...)'''

    #resolve errors
    #if err_res:

def rulematch( s, REs, AND=False ):
    '''s: string against which to evaulate the regular expression(s)
REs: regular expression or iterable of regular expressions (as strings) defining conditions to evaluate
AND: whether to test for all (True) or any (False) of the given regular expressions'''
    if type( REs ) == str:
        to_eval = { REs }
    else:
        to_eval = set( REs )
    evals = { re.fullmatch( RE, s ) for RE in to_eval }
    if AND:
        return all( evals )
    else:
        return any( evals )

def main():
    import argparse, re
    global AFFS, ROOTS, argparse, re, aff1

##    parser = argparse.ArgumentParser( description="Parse words into the morphemes they consist of." )
##    parser.add_argument( 

    plural=( 's', { '.*[oysz]' : 'es', 'person' : '', '.*u[sm]' : '' } )
    ortho1={ '.*y' : (-1, 'i'), '.*person' : (':', 'people'), '.*us' : ('-2:', 'i'), '.*um' : ('-2:', 'a') }
    group1=suffgroup(orthographic=ortho1,lexicon={'PL':plural},can_follow={'N'})
    AFFS={'1':group1}
    ROOTS={'N':{'bird','person'}}
    aff1=affix('PL','1')

if __name__ == '__main__':
    main()
