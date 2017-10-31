"""

Eric Nordstrom
Python 3.6.0
4/29/17

Removes out-of-vocabulary (OOV) words, a.k.a. "mixed words", from the provided series of
tokens. Words are deemed OOV when they are not found in either provided language dictionary.
Results are stored in .TXT file(s) specified by the user. PyDictionary option available for
English dictionary (requires PyDictionary module and reliable internet connection).

Example command line input:

    C:\Users\Me\Research\Files>..\Scripts\OOVs.py "Tokenized Corpus.txt" SpnDict . -d1 utf8

    Interpretation:
        ..\Scripts\OOVs.py          Call OOVs.py from separate directory
        "Tokenized Corpus.txt"      Corpus tokens data (quotes to avoid parsing argument)
        SpnDict                     Spanish dictionary (".txt" assumed)
        .                           PyDictionary option chosen for English dictionary
        -d1                         Spanish dictionary encoding type argument called
        utf8                        Spanish dictionary encoding type specification

"""


def PyDict(): #for default D2 argument in OOV_remove
    '''Returns PyDictionary object'''
    
    from PyDictionary import PyDictionary
    return PyDictionary()


def OOV_remove( tokens, D1, D2=PyDict() ):
    '''Removes OOVs from tokens list based on two dictionaries. PyDictionary module used for Dictionary 2 default.'''

    import string

    if type( D2 ) in { set, list, tuple, dict }:
        def condition3( word, D2 ): #condition for IF statement in FOR loop
            return word not in D2
        
    else: #assume PyDictionary
        
        def condition3( word, D2 ):
            return D2.meaning( word ) == None #This line would print to the console on each OOV if the STDOUT were not changed.

        import sys, os
        orig_stdout = sys.stdout #to save for later
        sys.stdout = open( os.devnull, 'w' ) #prevents printing to console during PyDictionary usage

    t = list( tokens ) #to become output tokens LIST with OOVs removed
    OOVs = {} #to become DICT containing removed OOVs hashed with their original indices in TOKENS
    d = 0 #index offset to account for already removed OOV words

    for i in range( 0, len(tokens) ):
        
        word = tokens[i]
        
        if word not in string.punctuation and word not in D1 and condition3( word, D2 ):
            OOVs.update({ i+1 : word }) #can remove "+1" after "i" on this line if zero-indexing desired.
            del t[i-d]
            d += 1

    if type( D2 ) not in { set, list, tuple, dict }:            
        sys.stdout = orig_stdout #restore stdout
    
    return ( t, OOVs )


def gettxt( file_name, encoding_type=None ):
    '''Reads and splits .TXT files. Appends ".txt" to file name if necessary.'''

    name = file_name

    if name[-4:] != ".txt":
        name += ".txt"

    return open( name, encoding=encoding_type ).read().split() #LIST type


def get_answer(prompt, accepted_answers, answer_type = str):
    '''Loops until input is an accepted answer'''

    answer = 'a;sdlkfha;oiwefhdnfaf;we'

    while answer not in accepted_answers:
        answer = answer_type( input( prompt ) )
        if answer.lower() not in accepted_answers:
            print( '"%s" is not an accepted response.' % str( answer ) )

    return answer


def destwrite( words, help_message ):
    '''User interface for writing to .TXT files. Does not return anything.'''
    
    destname = input( '\nInput destination .TXT file name ("\\H" for help): ' )
    h = True

    if destname.lower() == "\\h":
        print( help_message )
        destname = input( "\nInput destination .TXT file name: " )
        h = False

    option = 'n'
    sep = False #used for "append" case

    while option in { 'c', 'n' }: #determine how to open file

        if destname[-4:] != ".txt":
            destname += ".txt"
        
        try: #User should preferably type a file name that does not already exist, in which case this block is not necessary.
            
            dest = open( destname, 'r' )
            print( "\nFile by that name already exists." )
            prompt = 'Options:\n\t"O" - overwrite contents\n\t"A" - append to contents\n\t"C" - create new file with "(1)" appended to name\n\t"N" - enter new name\n\t[ctrl]+[C] - exit\n\nInput: '
            accepted_answers = { 'o', 'a', 'c', 'n', '\h' }
            option = get_answer( prompt, accepted_answers ).lower()

            if option == 'o':
                print( '\nOverwriting "%s".' % destname )
                dest = open( destname, 'w' )
            elif option == 'a':
                print( '\nAppending to "%s".' % destname )
                dest = open( destname, 'a' )
                sep = True
            elif option == 'c':
                destname = destname[:-4] + " (1)"
                
            elif option == 'n':
                destname = input( "\nInput destination .TXT file name%s: " % ( ' ("\\H" for help)' * h ) )
                
            else:
                print( help_message )
                destname = input( "\nInput destination .TXT file name: " )
                h = False
                
        except FileNotFoundError: #Preferred block

            option = '' #to exit WHILE loop
            print( '\nCreating and writing to new file "%s".' % destname )
            dest = open( destname, 'w' )

    dest.write( "\n"*9*sep ) #for "append" case

    for i in words:
        
            dest.write( str( i ) )

            if type( words ) == dict: #OOVs
                dest.write( " : " + words[i] )

            dest.write( "\n" )

    dest.close()
    print( "Writing complete. File saved." )

def main():
    import argparse
    parser = argparse.ArgumentParser( description = 'Locate, remove, and record out-of-vocabulary (OOV) words, a.k.a. "mixed words"' )

    parser.add_argument( "TOKENS", help="Name of the .TXT file containing corpus tokens." )
    parser.add_argument( "D1", help="Name of the language 1 dictionary .TXT file" )
    parser.add_argument( "D2", help='Name of the language 2 dictionary .TXT file. Enter "." for PyDictionary (requires PyDictionary module and reliable internet connection). NOTE: PyDictionary only for English; English dictionary must be D2 if using PyDictionary.' )
    parser.add_argument( "-t", "--TOKENS_encoding", help="Tokens .TXT file encoding type. Default used if not specified." )
    parser.add_argument( "-d1", "--D1_encoding", help="Language 1 dictionary .TXT file encoding type. Default used if not specified." )
    parser.add_argument( "-d2", "--D2_encoding", help="Language 2 dictionary .TXT file encoding type. Default used if not specified." )
    parser.add_argument( "-cd", "--change_directory", help='Change the folder in which to locate .TXT files. NOTE: It is also possible to specify individual file locations by including the entire path starting from "C:\".' )

    args = parser.parse_args()

    if args.change_directory:
        import os
        os.chdir( args.change_directory )

    tokens = gettxt( args.TOKENS, args.TOKENS_encoding )
    D1 = gettxt( args.D1, args.D1_encoding )

    if args.D2 == ".":

        if args.D2_encoding:
            raise RuntimeError( "Both PyDictionary option and encoding type specified for D2." )
        
        D2 = PyDict()
        
    else:
        D2 = gettxt( args.D2, args.D2_encoding )

    print( "\nRemoving OOVs...\n" )
    ( tokens_without_OOVs, OOVs ) = OOV_remove( tokens, D1, D2 )
    print( "\nOOVs removed.\n" )

    help_message = '\nDestination .TXT file used to store tokens list after removing out-of-vocabulary (OOV) words, a.k.a. "mixed words". If destination file to be outside of current working directory, include file location path in name.'
    destwrite( tokens_without_OOVs, help_message )

    prompt = "\nWrite removed OOVs to .TXT file? (Y/N): "
    accepted_answers = { 'y', 'n' }
    keep_OOVs = get_answer( prompt, accepted_answers )

    if keep_OOVs.lower() == 'y':
        help_message = '\nDestination .TXT file used to store removed out-of-vocabulary (OOV) words, a.k.a. "mixed words", and their corresponding locations in the original tokens list. If destination file to be outside of current working directory, include file location path in name.'
        destwrite( OOVs, help_message )

    print( "\nDone." )

if __name__ == "__main__":
    main()
