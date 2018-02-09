import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def _parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Compare sentence tokenizers on the input data")
    parser.add_argument(
        'input_file',
        help='file containing input data'
    )
    parser.add_argument(
        'tokenizers',
        nargs='+',
        help='names of tokenizers to compare'
    )
    parser.add_argument(
        '-t', '--tokenizer_location',
        default='',
        help='location of tokenizers (folder with .pickle files or .py script with tokenizer objects) if not the current working directory'
    )
    parser.add_argument(
        '-d', '--delimiter',
        default='\t',
        help='delimiter within lines. default: Tab'
    )
    parser.add_argument(
        '-a', '--abbreviations',
        nargs='+',
        help='abbreviations to add to the newly trained tokenizer'
    )
    parser.add_argument(
        '-c', '--token_column',
        default=0,
        type=int,
        help='column of data (0-indexed) containing word-level tokens. default: 0'
    )
    parser.add_argument(
        '-e', '--encoding',
        default='utf8',
        help='encoding type of input file'
    )
    parser.add_argument(
        '-o', '--omit_newly_trained',
        action='store_true',
        help='omit the automatic tokenizer trained on the input data'
    )
    parser.add_argument(
        '-l', '--log_level',
        help='change the log level'
    )
    logging.debug('Parsing user args...')
    args = parser.parse_args()
    if args.log_level:
        print('Setting log level to {}...'.format(args.log_level.upper()))
        logging.getLogger().setLevel(eval('logging.' + args.log_level.upper()))
    return args


def _loop_input(prompt):
    '''loop until user input interpreted as True or False'''
    i = ''
    while i.lower() not in {'y', 'yes', 'n', 'no'}:
        i = input(' '.join((prompt, '(Y/N) ')))
    return i in {'y', 'yes'}


def _report(ends, unique):
    '''report on the results'''
    print('Results were not all the same. Groups with the same results are as follow:')
    for name in unique:
        group = unique[name]
        group.add(name)
        print('\t' + ',  '.join(group))
    permission = _loop_input('Display results?')
    if permission:
        for name in unique:
            print('\nGroup: ' + name)
            print(' '.join((str(i) for i in ends[name])))


def compare(ends, tokenizer_names):
    '''compare the results of each tokenization'''
    logging.info('Comparing...')

    def rest(ends, name):
        r = dict(ends)
        r.pop(name)
        return r

    # eliminate non-unique results
    unique = {name: set() for name in tokenizer_names}
    for name in tokenizer_names:
        if name in unique:
            for compared_name in rest(ends, name):
                if ends[compared_name] == ends[name]:
                    unique.pop(compared_name)
                    unique[name].add(compared_name)

    # report
    if len(unique) == 1:
        print('All tokenizers gave the same results!')
    else:
        _report(ends, unique)


def main():

    # setup
    args = _parse_args()
    logging.info('Retrieving corpus data...')
    with open(args.input_file, 'r', encoding=args.encoding) as f:
        contents = f.read().splitlines()
    items = [line.split('\t') for line in contents]
    tokens = [line[args.token_column] for line in items]

    # get tokenizers
    tokenizers = []
    tokenizer_names = []
    # train new
    if not args.omit_newly_trained:
        logging.info('Training new tokenizer...')
        from train_sentence_tokenizer import Tokenizer
        tokenizers.append(Tokenizer(tokens, args.abbreviations if args.abbreviations else set()))
        tokenizer_names.append('newly trained')
    # user-specified
    if args.tokenizer_location and args.tokenizer_location.endswith('.py'):
        import os
        tokenizer_location_parts = args.tokenizer_location.split('\\')
        tokenizer_folder = '\\'.join(tokenizer_location_parts[:-1])
        tokenizer_script = '.'.join(tokenizer_location_parts[-1].split('.')[:-1])
        orig_wd = os.getcwd()
        os.chdir(tokenizer_folder)
        exec('import {} as module'.format(tokenizer_script), globals())
        os.chdir(orig_wd)
        for tokenizer in args.tokenizers:
            tokenizers.append(eval('module.' + tokenizer, globals()))
            tokenizer_names.append(tokenizer)
    else:
        from nltk.data import load
        for tokenizer in args.tokenizers:
            tokenizers.append(load('{}/{}.pickle'.format(args.tokenizer_location.replace('\\', '/'), tokenizer)))  # will this work?
            tokenizer_names.append(tokenizer)

    # get sentences
    ends = {name: [] for name in tokenizer_names}  # index of last token in each sentence per each tokenizer
    for i in range(len(tokenizers)):
        name = tokenizer_names[i]
        tokenizer = tokenizers[i]
        logging.info('Tokenizing with {}...'.format(name))
        sents = tokenizer.sentences_from_tokens(tokens)
        j = -1
        for sent in sents:
            L = len(sent)
            ends[name].append(j + L)
            j += L

    # compare
    compare(ends, tokenizer_names)

    # save
    if not args.omit_newly_trained:
        save = _loop_input('Save newly trained tokenizer as .pickle file?')
        if save:
            while save:
                try:
                    from pickle import dump
                    output_file = input('\nOutput folder & filename: ')
                    if not output_file.endswith('.pickle'):
                        output_file += '.pickle'
                    logging.info('Saving tokenizer to {}...'.format(output_file))
                    with open(output_file, 'wb') as f:
                        dump(tokenizers[0], f)
                    logging.info('Saved.')
                    save = False
                except Exception as ex:
                    logging.error('File not saved due to the following error:\n' + repr(ex))
    logging.warning('The results have not been saved. Copy them if desired; press Enter to end.')
    input()


if __name__ == '__main__':
    main()
