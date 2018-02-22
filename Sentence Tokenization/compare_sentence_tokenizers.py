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


def sentence_ends_by_tokenizer(tokens, **tokenizers):
    '''find the word-level token index of the last token in each sentence as found by each tokenizer. result is a dict of sets where the key is the name of the tokenizer as provided in **tokenizers.'''
    ends = {name: set() for name in tokenizers}  # index of last word-token in each sentence as found by each tokenizer
    for name in tokenizers:
        logging.info('Tokenizing with {}...'.format(name))
        sents = tokenizers[name].sentences_from_tokens(tokens)
        j = -1
        for sent in sents:
            L = len(sent)
            ends[name].add(j + L)
            j += L
    return ends


def _loop_input(prompt):
    '''loop until user input interpreted as True or False'''
    i = ''
    while i.lower() not in {'y', 'yes', 'n', 'no'}:
        i = input(prompt + ' (Y/N) ')
    return i in {'y', 'yes'}


class SharedAndUnique:
    '''class for viewing shared and unique values among sets. unique values are the values in the set of the outer key but not the set of the inner key.'''

    def __init__(self, **sets):
        '''sets with names'''
        self.unique = {outer: {inner: set() for inner in sets if inner != outer} for outer in sets}
        self.shared = set()
        for outer in sets:
            for val in outer:
                if val not in self.shared:
                    shared_with = {inner for inner in sets if inner != outer and val in sets[inner]}
                    if len(shared_with) == len(sets) - 1:
                        self.shared.add(val)
                    else:
                        not_in = {name for name in sets if name not in shared_with and name != outer}
                        for inner in not_in:
                            self.unique[outer][inner].add(val)

    def __str__(self):
        '''display unique results'''
        out = ''
        for outer in self.unique:
            for inner in self.unique[outer]:
                out += 'In {} but not in {}:\n{}\n\n'.format(outer, inner, self.unique[outer][inner])
        out = out.rstrip()
        return out


def _report(ends, unique):
    '''report on the results'''
    print('Results were not all the same. Groups with the same results are as follow:')
    for name in unique:
        group = unique[name]
        group.add(name)
        print('\t' + ',  '.join(group))
    permission = _loop_input('Display shared results?')
    if permission:
        for name in unique:

            print('\nGroup: ' + name)
            print(' '.join((str(i) for i in ends[name])))


def compare(ends):
    '''compare the results of each tokenization'''
    logging.info('Comparing...')

    def rest(ends, name):
        r = dict(ends)
        r.pop(name)
        return r

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
    tokenizers = {}
    # train new
    if not args.omit_newly_trained:
        logging.info('Training new tokenizer...')
        from train_sentence_tokenizer import Tokenizer
        tokenizers['Newly Trained'] = Tokenizer(tokens, args.abbreviations if args.abbreviations else set())
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
        for name in args.tokenizers:
            tokenizers[name] = eval('module.' + name, globals())
    else:
        from nltk.data import load
        for name in args.tokenizers:
            tokenizers[name] = load('{}/{}.pickle'.format(args.tokenizer_location.replace('\\', '/'), name))

    # get sentences
    ends = sentence_ends_by_tokenizer(tokens, **tokenizers)

    # compare
    compare(ends)

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
