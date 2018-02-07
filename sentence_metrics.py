"""
Eric Nordstrom
Python 3.6.0
2/5/2018

Get metrics on each sentence of a corpus individually.
"""


from copy import copy
import logging
STARTS = -1  # markers on first token of sentence
ENDS = 0  # markers on last token of sentence
marker_type = ENDS  # adjust this according to data

# logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
logging.LBL = 5  # line-by-line: more verbose than DEBUG as it logs on every line of data
logging.addLevelName(logging.LBL, 'LBL')
logging.lbl = lambda msg, *args, **kwargs: logging.log(logging.LBL, msg, *args, **kwargs)


def metrics(funcs, args, markers):
    '''\
generator of generators for the result of each function on each sentence
`args`: lang & POS values for each token
`markers`: indices indicating sentence marker locations\
    '''

    # debugging
    try:
        LA = len(args)
    except TypeError:
        LA = 'N/A'
    try:
        LM = len(markers)
    except TypeError:
        LM = 'N/A'
    logging.debug('''\
metrics: Executing with the following inputs:
    Functions: {}
    Lang & POS args of type {}
    Number of lang/POS arg rows: {}
    Markers of type {}
    Number of markers: {}\
'''.format(funcs, type(args), LA, type(markers), LM))

    def lbl(sent):
        if logging.LBL >= logging.getLogger().level:
            msg = 'metrics: Sentence:\n'
            for line in sent:
                msg += '\t{}\n'.format(line)
            logging.lbl(msg)

    # setup
    ai, mi = iter(args), iter(markers)
    try:  # test whether `funcs` is iterable
        for func in copy(funcs):
            break
    except TypeError:
        funcs = {funcs}  # assert iterability
    if marker_type is STARTS and not next(copy(mi)):  # skip first marker if right at beginning
        logging.debug('Skipping first marker...')
        next(mi)

    # compute bulk
    i = 0
    for marker in mi:
        sent = []
        while i <= marker + marker_type:
            sent.append(next(ai))
            i += 1
        lbl(sent)
        yield (func(sent) for func in funcs)

    # might have one more sentence if no marker at end
    lastsent = []
    end = False
    while not end:
        try:
            lastsent.append(next(ai))
            i += 1
        except StopIteration:
            end = True
    if lastsent:
        lbl(lastsent)
        yield (func(lastsent) for func in funcs)


def get_marker_indices(lines, marker_col=None, marker=None):
    '''extract markers as a series of row/token indices'''

    # debugging
    try:
        L = len(lines)
    except TypeError:
        L = 'N/A'
    logging.debug('''\
get_marker_indices: Executing with the following inputs...
    Lines of type {}
    Number of lines: {}
    Marker column: {}
    Marker: {}\
'''.format(type(lines), L, marker_col, marker))

    # establish marker column
    if marker_col is None:
        row1 = next(copy(lines))
        logging.warning('No marker column specified. Setting marker column to {}...'.format(len(row1) - 1))
        try:
            marker_col = len(row1) - 1  # assume marker column is the last column
        except TypeError:
            pass  # rows found not to be subscriptable

    # create marker detection function
    if marker:
        def md(val):
            return val == marker
    else:
        def md(val):
            return val

    # create marker column value function
    if marker_col is None:
        def mcv(row):
            return row
    else:
        def mcv(row):
            return row[marker_col]

    # compute
    for i, line in enumerate(lines):
        val = mcv(line)
        detected = md(val)
        logging.lbl('get_marker_indices: Row {}: {}: {}'.format(i, val, detected))
        if detected:
            yield i


def metric_args(lines, lang_col=None, POS_col=None):
    '''translate each line of data into a dict of lang and POS values'''

    # debugging
    try:
        L = len(lines)
    except TypeError:
        L = 'N/A'
    logging.debug('''\
metric_args: Executing with the following inputs:
    Lines of type {}
    Number of lines: {}
    Language column: {}
    POS column: {}\
'''.format(type(lines), L, lang_col, POS_col))

    # compute
    for line in lines:
        args = {}
        if lang_col:
            args['lang'] = line[lang_col]
        if POS_col:
            args['POS'] = line[POS_col]
        logging.lbl('metrics_args: {}'.format(args))
        yield args


def preprocess(lines, delimiter):
    '''split each line by the delimiter'''
    logging.debug('preprocess: Splitting lines by delimiter {}...'.format(repr(delimiter)))
    for i, line in enumerate(lines):
        lines[i] = line.split(delimiter)


def file_metrics(funcs, file, delimiter, first_row=True, lang_col=None, POS_col=None, marker_col=None, marker=None):
    '''perform sentence-level metrics on file contents'''

    # debugging
    logging.debug('''\
file_metrics: Executing with the following inputs:
    Functions: {}
    File: {}
    Delimiter: {}
    Language column: {}
    POS column: {}\
'''.format(funcs, file, delimiter, lang_col, POS_col))

    # setup
    logging.debug('file_metrics: Setting up...')
    lines = file.read().splitlines()
    if not first_row:
        logging.debug('file_metrics: Skipping first row...')
        lines.pop(0)
    preprocess(lines, delimiter)

    # extract args and markers
    logging.debug('file_metrics: Retrieving lang & POS args...')
    args = metric_args(lines, lang_col, POS_col)
    logging.debug('file_metrics: Locating sentence markers...')
    markers = get_marker_indices(lines, marker_col, marker)

    # compute metrics
    logging.debug('file_metrics: Computing metrics...')
    return metrics(funcs, args, markers)


def _ap_parser():
    '''set up and return the argparse parser'''
    import argparse
    logging.debug('_ap_parser: Creating argument parser...')
    parser = argparse.ArgumentParser(description='Sentence-level metrics on data with sentence markers. **Not yet debugged**')  # DEBUG
    parser.add_argument(
        'input_file',
        help='corpus file with sentence markers'
    )
    parser.add_argument(
        'lang_col',
        type=int,
        help='column containing language tags (0-indexed)'
    )
    parser.add_argument(
        'POS_col',
        type=int,
        help='column containing POS tags (0-indexed)'
    )
    parser.add_argument(
        'marker_col',
        type=int,
        help='column containing sentence markers (0-indexed)'
    )
    parser.add_argument(
        'function_file',
        help='Python file containing function(s) to evaluate. function should take an argument of a list of dicts in the format {"lang": lang_val, "POS": POS_val}. if in separate files, must join into single file.'
    )
    parser.add_argument(
        'function_names',
        nargs='+',
        help='series of function names in function file. all functions will be performed on each sentence.'
    )
    parser.add_argument(
        '-m', '--marker',
        help='marker string. if not specified, only empty entries in the marker column are ignored.'
    )
    parser.add_argument(
        '-d', '--delimiter',
        default='\t',
        help='delimiter between columns. default: Tab'
    )
    parser.add_argument(
        '-f', '--skip_first_row',
        action='store_true',
        help='specify if the first row of the input file contents is to be skipped'
    )
    parser.add_argument(
        '-mt', '--marker_type',
        default='ENDS',
        help='STARTS (first word of sentence) or ENDS (last word of sentence). default: ENDS'
    )
    parser.add_argument(
        '-e', '--encoding',
        default='utf8',
        help='encoding type of input file. default: utf8'
    )
    parser.add_argument(
        '-o', '--output_folder',
        default=orig_wd,
        help='location to save output file with metrics'
    )
    parser.add_argument(
        '-l', '--log_level',
        help='Change the log level'
    )
    return parser


def main():
    '''for command line execution'''

    # setup
    print()
    import os
    from datetime import datetime as dt
    from csv import writer
    global orig_wd, marker_type
    orig_wd = os.getcwd()
    cmd_args = _ap_parser().parse_args()
    if cmd_args.log_level:
        print('Setting log level to {}...'.format(cmd_args.log_level.upper()))
        logging.getLogger().setLevel(eval('logging.' + cmd_args.log_level.upper()))
    logging.info('Setting up...')
    logging.debug('Setting marker type to {}...'.format(cmd_args.marker_type))
    marker_type = eval(cmd_args.marker_type)
    input_filename = cmd_args.input_file.split('\\')[-1]
    input_file_title, input_file_extn = tuple(input_filename.split('.'))
    output_filename = 'Metrics on "{}" ({}).{}'.format(input_file_title, dt.now(), input_file_extn)
    output_file = '{}\\{}'.format(cmd_args.output_folder, output_filename.replace(':', '.'))
    logging.debug('Output file will be: ' + output_file)

    # get function(s)
    logging.info('Retrieving functions...')
    input_file_parts = cmd_args.function_file.split('\\')
    logging.debug('Input file parts = {}'.format(input_file_parts))
    folder = '\\'.join(input_file_parts[:-1])
    logging.debug('Folder = ' + folder)
    filename = input_file_parts[-1]
    if filename.endswith('.py'):
        filename = filename[:-3]
    logging.debug('File name = ' + filename)
    if folder:
        os.chdir(folder)
        logging.debug('Changed directory to ' + os.getcwd())
    exec('import {} as module'.format(filename), globals())
    logging.debug('Module imported: {}'.format(module))
    os.chdir(orig_wd)
    logging.debug('Changed directory to ' + os.getcwd())
    funcs = [module.__dict__[funcname] for funcname in cmd_args.function_names]
    logging.debug('Functions list: {}'.format(funcs))

    # load input file & make generator
    logging.info('Retrieving input file contents...')
    with open(cmd_args.input_file, encoding=cmd_args.encoding.lower()) as f:
        sent_metrics = file_metrics(funcs, f, cmd_args.delimiter, not cmd_args.skip_first_row, cmd_args.lang_col, cmd_args.POS_col, cmd_args.marker_col, cmd_args.marker)

    # compute & write to output file
    logging.info('Computing and writing to output file...')
    with open(output_file, 'w', encoding=cmd_args.encoding.lower(), newline='\n') as f:
        writer = writer(f, delimiter='\t')
        writer.writerow(['Sentence No.'] + [func.__name__ for func in funcs])  # headings
        for i, metrics in enumerate(sent_metrics):
            writer.writerow([i] + [metric for metric in metrics])
    logging.info('Wrote to output file at ' + output_file)

    print('\nDone')


if __name__ == '__main__':
    main()
