"""
Eric Nordstrom
Python 3.6.0
2/8/2018
For training new sentence tokenizers and saving as a .pickle file
"""

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def _parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="")
    parser.add_argument(
        'training_file',
        help='file containing training data'
    )
    parser.add_argument(
        'name',
        help='desired name for trained tokenizer output'
    )
    parser.add_argument(
        '-a', '--abbreviations',
        nargs='+',
        help='abbreviations to add to the tokenizer parameters (only internal punctuation, e.g. "mr"; "ph.d")'
    )
    parser.add_argument(
        '-o', '--output_folder',
        help='folder in which to save trained tokenizer output (default: current working directory)'
    )
    parser.add_argument(
        '-c', '--token_column',
        help='column containing word-level tokens'
    )
    parser.add_argument(
        '-l', '--log_level',
        help='change the log level'
    )
    parser.add_argument(
        '-e', '--encoding',
        default='utf8',
        help='encoding type (default: UTF-8)'
    )
    logging.debug('Parsing user args...')
    args = parser.parse_args()
    if args.log_level:
        print('Setting log level to {}...'.format(args.log_level.upper()))
        logging.getLogger().setLevel(eval('logging.' + args.log_level.upper()))
    return args


def Tokenizer(tokens, abbreviations=set()):
    '''create a Punkt tokenizer'''
    from nltk.tokenize import punkt
    logging.info('Training tokenizer...')
    trainer = punkt.PunktTrainer()
    trainer.train_tokens(tokens)
    logging.debug('Creating tokenizer object...')
    tokenizer = punkt.PunktSentenceTokenizer(trainer.get_params())
    if abbreviations:
        logging.info('Adding abbreviations...')
    for abbrev in abbreviations:
        tokenizer._params.abbrev_types.add(abbrev.lower())
    return tokenizer


def main():
    from pickle import dump

    # setup
    args = _parse_args()
    output_folder = args.output_folder if args.output_folder else ''
    output_file = '{}\\{}.pickle'.format(output_folder, args.name)
    logging.debug('Output file will be: ' + output_file)

    # get input
    logging.info('Retrieving training data')
    with open(args.input_file, 'r', encoding=args.encoding) as f:
        contents = f.read().splitlines()
    logging.debug('Preprocessing training data...')
    items = [line.split['\t'] for line in contents]
    tokens = [line[0] for line in items]

    # train
    tokenizer = Tokenizer(tokens, args.abbreviations if args.abbreviations else set())

    # write
    logging.info('Saving tokenizer to {}...'.format(output_file))
    with open(output_file, 'wb') as f:
        dump(tokenizer, f)


if __name__ == '__main__':
    main()
