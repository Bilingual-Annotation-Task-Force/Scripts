"""
Eric Nordstrom
Python 3.6.0
10/30/17
"""

#Link: http://textminingonline.com/dive-into-nltk-part-ii-sentence-tokenize-and-word-tokenize
#This script uses Punkt via nltk.data. According to the above webpage, Punkt supports 17 European languages.
#Refer to the above link for instructions to download nltk.data

def main():
    import argparse, nltk.data, os
    orig_wd = os.getcwd()
    
    parser = argparse.ArgumentParser( description = "Writes 2 files: (1) sentence-tokenized corpus text and (2) indices at which each sentence starts." )
    parser.add_argument( 'text', help="corpus text file" )
    parser.add_argument( 'language', help="language of this corpus" )
    parser.add_argument( '-e', '--encoding', default='utf8', help="encoding of input file (default=UTF8)" )
    parser.add_argument( '-tf', '--tokenizers_folder', help="folder in which the 'tokenizers' folder resides" )
    parser.add_argument( '-of', '--output_folder', help="folder to write output files" )
    parser.add_argument( '-o', '--omit', help="omit writing of one of the output files (1 or 2)" )
    args = parser.parse_args()

    if args.tokenizers_folder:
        os.chdir( args.tokenizers_folder )
    tokenizer = nltk.data.load( 'tokenizers/punkt/' + args.language + '.pickle' )
    os.chdir( orig_wd )
    intext = open( args.text, encoding=args.encoding ).read()
    print( '\nTokenizing...' )
    sents = tokenizer.tokenize( intext )
    print( '\nTokenized.' )

    if args.text.lower().endswith('.txt'):
        firstpart = args.text[:-4]
    else:
        firstpart = args.text

    outtext = indices = '' #for outfiles 1 and 2, respectively
    searchstart = 0
    print( '\nCreating output file contents...' )

    for i in range(0,len(sents)):
        sent = sents[i]
        outtext += sent + '\n'
        index = searchstart + intext[searchstart:].find(sent) #in case characters are lost b/w sentences after tokenizing (e.g. carriage return)
        indices += str( index ) + ' '
        searchstart = index + len( sent )

    if args.output_folder:
        print( args.output_folder )
        os.chdir( args.output_folder )
    print( '\nWriting output file 1...' )        
    outfilename = firstpart + ' (sentence-tokenized).txt'
    outfile1 = open( outfilename, 'w', encoding=args.encoding )
    outfile1.write( outtext )
    outfile1.close()
    print( '\nOutput file #1 complete. Writing output file 2...' )
    outfilename = firstpart + ' (sentence indices).txt'
    outfile2 = open( outfilename, 'w', encoding=args.encoding )
    outfile2.write( indices )
    outfile2.close()
    print( '\nOutput file #2 complete.' )

    print( '\nDone.' )

if __name__ == "__main__":
    main()
