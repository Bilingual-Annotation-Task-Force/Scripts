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
from string import punctuation
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def _ap_parser():
    '''set up and return the argparse parser'''
    import argparse
    parser = argparse.ArgumentParser(description="Outputs a new TSV file with an additional column indicating the last token of each sentence. Input can be tokenized or untokenized at the word level.")
    parser.add_argument(
        'input_file',
        help="corpus file"
    )
    parser.add_argument(
        'tokenizer',
        help="the desired sentence tokenizer *.pickle file"
    )
    parser.add_argument(
        '-wt', '--word_tokenized',
        action='store_true',
        help="specify if the input is already tokenized at the word level"
    )
    parser.add_argument(
        '-e', '--encoding',
        default='utf8',
        help="file encoding (default=UTF8)"
    )
    parser.add_argument(
        '-of', '--output_folder',
        help="folder to write output files"
    )
    parser.add_argument(
        '-tc', '--token_column',
        # no default; this way, can check if user specified
        type=int,
        help="index of column containing word-level tokens (default: 0)"
    )
    parser.add_argument(
        '-d', '--delimiter',
        # no default; this way, can check if user specified
        help="delimter between columns in input file (default: Tab)"
    )
    parser.add_argument(
        '-l', '--log_level',
        help="change the log level"
    )
    return parser


def wordtok(sent):
    '''tokenize at the word level'''
    result = sent.strip().split()
    i = 0
    while i < len(result):
        word = result[i]
        j = k = 0
        while word[j] in punctuation:
            j += 1
        while word[-1 - k] in punctuation:
            k += 1
        L = len(word)
        if j + k < L:  # not all punctuation
            result[i] = word[j:L - k]
            if j > 0:
                result.insert(i, word[:j])
                i += 1
                result.insert(i + 1, word[-k:])  # might want to do more to separate out '.' from '"', etc.
                i += 1
        i += 1
    return result


def main():
    # set up
    import os
    import nltk.data
    import csv
    orig_wd = os.getcwd()
    toks = indices = None
    args = _ap_parser().parse_args()
    if args.log_level:
        logging.getLogger().setLevel(eval('logging.' + args.log_level.upper()))
    print('')

    # some file name processing
    infile_parts = args.input_file.split('\\')[-1].split('.')
    infile_ext = infile_parts[-1].lower()
    infile_name = '.'.join(infile_parts[:-1])
    tknzr_name = args.tokenizer.replace('\\', '/')
    if not tknzr_name.endswith('.pickle'):
        tknzr_name += '.pickle'

    # pre-process input file contents
    logging.info('Pre-processing input file...')
    lines = open(args.input_file, encoding=args.encoding).readlines()
    token_column = args.token_column if args.token_column else 0
    if args.word_tokenized or args.delimiter is not None or args.token_column is not None:
        logging.info('Interpreting as tokens at word level.')
        wt = True
        corptext = [''] * len(lines)
        for i, line in enumerate(lines):
            lines[i] = line.strip().split(args.delimiter)
            corptext[i] = lines[i][token_column]
    else:
        logging.info('Interpreting as untokenized at word level (will tokenize).')
        wt = False
        corptext = '\n'.join(lines)

    # get tokenizer
    logging.info('Loading Punkt tokenizer...')
    tokenizer = nltk.data.load(tknzr_name)

    # tokenize
    logging.warning('Note: Custom-trained sentence tokenizers are best for multilingual data.')
    logging.info('Tokenizing...')
    if wt:
        sents = tokenizer.sentences_from_tokens(corptext)
    else:
        sents = tokenizer.sentences_from_text(corptext)

    # write to output file
    os.chdir(orig_wd)
    if args.output_folder:
        os.chdir(args.output_folder)
    lastpart = ' (marked for sentence ends).tsv'
    outfilename = infile_name + lastpart
    with open(outfilename, 'w', encoding=args.encoding) as outfile:
        if args.encoding == 'utf8':  # other encoding types might have the same problem; haven't checked yet
            csv.register_dialect('utf8-TSV', 'excel-tab', lineterminator='\n')
            dialect = 'utf8-TSV'
        else:
            dialect = 'excel-tab'
        writer = csv.writer(outfile, dialect)
        if wt:
            logging.info('Writing to output file...')
            start = c = 0  # DEBUG
            for sent in sents:
                c += 1  # DEBUG
                L = len(sent)
                for i, tok in enumerate(sent):
                    line = lines[start + i]
                    if line[token_column] != tok:
                        logging.error("Token mismatch at line {}: '{}' != '{}'".format(start + i, tok, line[token_column]))
                    if i == L - 1:
                        line += ['SENT']
                    else:
                        line += ['']
                    writer.writerow(line)
                start += L
        else:
            logging.info('Word-tokenizing and writing to output file...')
            for sent in sents:
                toks = wordtok(sent)
                L = len(toks)
                for i, tok in enumerate(toks):
                    if i == L - 1:
                        line = [tok, 'SENT']
                    else:
                        line = [tok, '']
                    writer.writerow(line)
    print(c)  # DEBUG
    logging.info('Done.')


if __name__ == "__main__":
    main()
