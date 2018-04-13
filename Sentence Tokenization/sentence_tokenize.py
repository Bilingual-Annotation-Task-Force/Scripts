"""
Eric Nordstrom
Python 3.6.0
11/15/17
"""


import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def _ap_parser():
    '''set up and return the argparse parser'''
    import argparse
    parser = argparse.ArgumentParser(description='''\
Outputs a new TSV file with an additional column indicating the last token of each sentence. Input can be tokenized or untokenized at the word level. If no pre-trained tokenizer specified, this script splits \
the corpus into `n` subsections, each of which is in turn split in half. Two tokenizers are then trained: one on the first half of each section and the other on the \
second half. Each tokenizer is applied to the opposite half from which it was trained.\
''')
    parser.add_argument(
        'input_file',
        help="corpus file"
    )
    parser.add_argument(
        '-t', '--tokenizer',
        help="pre-trained sentence tokenizer *.pickle file"
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


def main():
    # set up
    import os
    import nltk.data
    import csv
    orig_wd = os.getcwd()
    toks = None
    args = _ap_parser().parse_args()
    if args.log_level:
        logging.getLogger().setLevel(eval('logging.' + args.log_level.upper()))
    print('')

    # some file name processing
    infile_parts = args.input_file.split('\\')[-1].split('.')
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
            start = 0
            for sent in sents:
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
            from nltk.tokenize import word_tokenize as wordtok  # can replace with other word tokenizer if desired
            for sent in sents:
                toks = wordtok(sent)
                L = len(toks)
                for i, tok in enumerate(toks):
                    if i == L - 1:
                        line = [tok, 'SENT']
                    else:
                        line = [tok, '']
                    writer.writerow(line)
    logging.info('Done.')


if __name__ == "__main__":
    main()
