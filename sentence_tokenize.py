"""
Eric Nordstrom
Python 3.6.0
11/2/17
"""

#Referred to this link for sentence tokenizer: http://textminingonline.com/dive-into-nltk-part-ii-sentence-tokenize-and-word-tokenize
#This script uses Punkt via nltk.data. According to the above webpage, Punkt supports 17 European languages.
#The above link has instructions for downloading necessary files.

def ispunc( TOK ):
    '''whether a token consists only of punctuation characters'''
    return all([char in punc for char in TOK])
    
def join_tokens( INTEXT ):
    '''Combine first column of .tsv contents into a corpus for later sentence tokenization. Also returns input contents split into lines.'''
    global punc
    from string import punctuation as punc
    lines = INTEXT.splitlines()
    corptext = ''
    for line in lines:
        tok = line.split('\t')[0]
        if not(ispunc( tok )):
            corptext += ' '
        corptext += tok
    corptext = corptext.lstrip( ' ' )
    return corptext, lines

def disp_extns( extns, conj ):
    '''display a list of accepted file extensions in verbose form'''
    disp = '.' + extns[-1]
    L = len( extns )
    if L > 1:
        disp = ' ' + conj + ' ' + disp
        if L > 2:
            disp = ',' + disp
        disp = '.' + ', .'.join( extns[:-1] ) + disp
    return disp

def main( accepted_file_types=['txt','tsv'],
          tsv_sentstart_mark='start' ):
    
    #setup
    import argparse, nltk.data, os
    orig_wd = os.getcwd()
    toks = indices = None
    print('')

    #get args
    parser = argparse.ArgumentParser( description = "For .txt input, writes 2 .txt files: (1) sentence-tokenized corpus text and (2) indices at which each sentence starts. For .tsv input, writes an output .tsv file with an additional column indicating the first token of each sentence." )
    parser.add_argument( 'text',
                         help="corpus file (%s)" % disp_extns( accepted_file_types, 'or' ) )
    parser.add_argument( 'language',
                         help="desired language of Punkt tokenizer model" )
    parser.add_argument( '-e', '--encoding',
                         default='utf8',
                         help="file encoding (default=UTF8)" )
    parser.add_argument( '-tf', '--tokenizers_folder',
                         help="folder in which the 'tokenizers' folder resides" )
    parser.add_argument( '-of', '--output_folder',
                         help="folder to write output files" )
    args = parser.parse_args()

    #some file name processing
    infile_parts = args.text.split('\\')[-1].split('.')
    infile_ext = infile_parts[-1].lower()
    infile_name = '.'.join( infile_parts[:-1] )

    #pre-process input file contents
    print( 'Pre-processing input file...\n' )
    intext = open( args.text, encoding=args.encoding ).read()
    if infile_ext == 'tsv':
        corptext, toks = join_tokens( intext )
    elif infile_ext == 'txt':
        corptext = intext
    else:
        raise RuntimeError( 'Only %s allowed.' % disp_extns( accepted_file_types, 'and' ) )

    #get tokenizer
    if args.tokenizers_folder:
        path = args.tokenizers_folder.split('\\')
        if path[-1].lower() == 'punkt':
            if path[-2].lower() == 'tokenizers':
                n = 2
            else:
                n = 1
            path = path[:-n]
        elif path[-1].lower() == 'tokenizers':
            path = path[:-1]
        folder = '\\'.join( path )
        os.chdir( folder )
    tokenizer = nltk.data.load( 'tokenizers/punkt/' + args.language + '.pickle' )

    #tokenize
    print( 'Tokenizing...\n' )
    sents = tokenizer.tokenize( corptext )
    nsents = len( sents )

    #get output contents
    print( 'Creating output file contents...\n' )
    if infile_ext == 'txt':
        outtext = indices = ''
        searchstart = 0
        for i in range( nsents ):
            sent = sents[i]
            outtext += sent + '\n'
            index = searchstart + intext[searchstart:].find( sent ) #in case characters are lost b/w sentences after tokenizing (e.g. newline; others possible?)
            indices += str( index ) + ' '
            searchstart = index + len( sent )
    else:
        rownum = 0
        for i in range( nsents ):
            toks[rownum] += '\t' + tsv_sentstart_mark #mark start of sentence
            sent = sents[i]
            sentlen = len( sent ) - sent.count( ' ' )
            lencount = 0
            while lencount < sentlen:
                lencount += len( toks[rownum].split('\t')[0] )
                rownum += 1
            if lencount > sentlen:
                raise RuntimeError( 'Sentence length mismatch at sentence #%s.' % ( i + 1 ) )
        outtext = '\n'.join( toks )

    #write to output file(s)
    os.chdir( orig_wd )
    if args.output_folder:
        os.chdir( args.output_folder )
    print( 'Writing output file(s)...\n' )
    if infile_ext == 'txt':
        lastpart = ' (sentence-tokenized).txt'
    else:
        lastpart = ' (marked for sentence starts).tsv'
    outfilename = infile_name + lastpart
    outfile = open( outfilename, 'w', encoding=args.encoding )
    outfile.write( outtext )
    outfile.close()
    if infile_ext == 'txt':
        outfilename = infile_name + ' (sentence indices).txt'
        outfile2 = open( outfilename, 'w', encoding=args.encoding )
        outfile2.write( indices )
        outfile2.close()

    print( 'Done.' )

if __name__ == "__main__":
    main()
