"""
Eric Nordstrom
Python 3.6.0
11/15/17
"""

# Referred to this link to obtain the sentence tokenizer: http://textminingonline.com/dive-into-nltk-part-ii-sentence-tokenize-and-word-tokenize
# This script uses Punkt via the module nltk.data. According to the above webpage, Punkt supports 17 European languages.
# The above link has instructions for downloading necessary files.
# Further instructions are in the argparse help message.
# Note: this tokenization will be imperfect for multilingual data because there is not yet a way to combine sentence tokenizers of multiple languages; one must be picked, and resulting
#    sentences will have to be screened to ensure correct tokenization.

# Example command line input:
#     ..\dropbox\documents\compling\bats\"scripts (github)"\sentence_tokenize.py test.tsv english -tf ..\anaconda3\lib\site-packages
#
#     Explanation:
#        This is the input I used to test the file. My working directory at the time of execution was the desktop, where I kept the input file "test.tsv"; hence, no address was necessary
#        to specify the location of the file. The argument preceding "test.tsv" calls this script, which I keep in a folder called "Scripts (GitHub)". The third argument is the language
#        of the selected tokenizer, or more specifically the name of the Punkt tokenizer ".pickle" file (a typo would cause a lookup error). Finally, I specified an optional argument
#        instructing the script to locate the tokenizers folder in my Anaconda files where I have downloaded it and where it does not automatically check. Without additional arguments,
#        the script writes the output file to the original working directory. Since it is a .tsv file, the result is a new .tsv with the original name followed by "(marked for sentence
#        starts)" and contents including a new column marking the start of each sentence.


import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def _ispunc(TOK):
    '''whether a token consists only of punctuation characters'''
    return all([char in punc for char in TOK])


def join_tokens(INTEXT):
    '''Combine first column of .tsv contents into a corpus for later sentence tokenization. Also returns input contents split into lines.'''
    global punc
    from string import punctuation as punc
    lines = INTEXT.splitlines()
    corptext = ''
    ncols = 0
    for line in lines:
        items = line.split('\t')
        tok = items[0]
        if len(items) > ncols:
            ncols = len(items)
        if not(_ispunc(tok)):
            corptext += ' '
        corptext += tok
    del punc
    corptext = corptext.lstrip(' ')
    return corptext, lines, ncols


def _disp_extns(extns, conj):
    '''display a list of accepted file extensions in verbose form'''
    disp = '.' + extns[-1]
    L = len(extns)
    if L > 1:
        disp = ' ' + conj + ' ' + disp
        if L > 2:
            disp = ',' + disp
        disp = '.' + ', .'.join(extns[:-1]) + disp
    return disp


def _ap_parser(accepted_file_types):
    '''set up and return the argparse parser'''
    import argparse
    parser = argparse.ArgumentParser(description="For .txt input, writes 2 .txt files: (1) sentence-tokenized corpus text and (2) indices at which each sentence starts. For .tsv input, writes an output .tsv file with an additional column indicating the first token of each sentence.")
    parser.add_argument(
        'text',
        help="corpus file ({})".format(_disp_extns(accepted_file_types, 'or'))
    )
    parser.add_argument(
        'language',
        help="desired language of Punkt tokenizer model"
    )
    parser.add_argument(
        '-e', '--encoding',
        default='utf8',
        help="file encoding (default=UTF8)"
    )
    parser.add_argument(
        '-tf', '--tokenizers_folder',
        help="folder in which the 'tokenizers' folder resides"
    )
    parser.add_argument(
        '-of', '--output_folder',
        help="folder to write output files"
    )
    parser.add_argument(
        '-l', '--log_level',
        help="change the log level"
    )
    return parser
    from argparse import ArgumentParser
    parser = ArgumentParser(description="")
    parser.add_argument(
        '-l', '--log_level',
        help="change the log level"
    )


def _interpret_tokenizers_folder(user_input):
    '''interpret the user input for the location of the folder containing the `tokenizers` subfolder'''
    folders = user_input.split('\\')
    if folders[-1].lower() == 'punkt':
        if folders[-2].lower() == 'tokenizers':
            n = 2
        else:
            n = 1
        folders = folders[:-n]
    elif folders[-1].lower() == 'tokenizers':
        folders = folders[:-1]
    return '\\'.join(folders)


def main(accepted_file_types=['txt', 'tsv'], tsv_sentstart_mark='start'):

    # setup
    import os
    import nltk.data
    orig_wd = os.getcwd()
    toks = indices = None
    args = _ap_parser().parse_args()
    if args.log_level:
        logging.getLogger().setLevel(eval('logging.' + args.log_level.upper()))
    print('')

    # some file name processing
    infile_parts = args.text.split('\\')[-1].split('.')
    infile_ext = infile_parts[-1].lower()
    infile_name = '.'.join(infile_parts[:-1])

    # pre-process input file contents
    logging.info('Pre-processing input file...')
    intext = open(args.text, encoding=args.encoding).read().strip()
    if infile_ext == 'tsv':
        corptext, toks, ncols = join_tokens(intext)
    elif infile_ext == 'txt':
        corptext = intext
    else:
        raise RuntimeError('Only {} allowed.'.format(_disp_extns(accepted_file_types, 'and')))

    # get tokenizer
    logging.info('Locating Punkt tokenizer...')
    if args.tokenizers_folder:
        os.chdir(_interpret_tokenizers_folder(args.tokenizers_folder))
    tokenizer = nltk.data.load('tokenizers/punkt/{}.pickle'.format(args.language))

    # tokenize
    logging.warning('Note: Custom-trained sentence tokenizers are best for multilingual data.')
    logging.info('Tokenizing...')
    sents = tokenizer.tokenize(corptext)
    nsents = len(sents)

    # get output contents
    logging.info('Creating output file contents...')
    if infile_ext == 'txt':
        outtext = indices = ''
        searchstart = 0
        for i in range(nsents):
            sent = sents[i]
            outtext += sent + '\n'
            index = searchstart + intext[searchstart:].find(sent)  # in case characters are lost b/w sentences after tokenizing (e.g. newline; others possible?)
            indices += str(index) + ' '
            searchstart = index + len(sent)
    else:
        rownum = 0
        for i in range(nsents):
            toks[rownum] += '\t' * (ncols - toks[rownum].count('\t')) + tsv_sentstart_mark  # mark start of sentence. NCOLS considered in case of inconsistent number of entries per row.
            sent = sents[i]
            sentlen = len(sent) - sent.count(' ')
            lencount = 0
            while lencount < sentlen:
                lencount += len(toks[rownum].split('\t')[0])
                rownum += 1
            if lencount > sentlen:
                raise RuntimeError('Sentence length mismatch at sentence #{}.'.format(i + 1))
        outtext = '\n'.join(toks)

    # write to output file(s)
    os.chdir(orig_wd)
    if args.output_folder:
        os.chdir(args.output_folder)
    logging.info('Writing output file(s)...')
    if infile_ext == 'txt':
        lastpart = ' (sentence-tokenized).txt'
    else:
        lastpart = ' (marked for sentence starts).tsv'
    outfilename = infile_name + lastpart
    outfile = open(outfilename, 'w', encoding=args.encoding)
    outfile.write(outtext)
    outfile.close()
    if infile_ext == 'txt':
        outfilename = infile_name + ' (sentence indices).txt'
        outfile2 = open(outfilename, 'w', encoding=args.encoding)
        outfile2.write(indices)
        outfile2.close()

    logging.info('Done.')


if __name__ == "__main__":
    main()
