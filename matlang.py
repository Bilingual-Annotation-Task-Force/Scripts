"""
Eric Nordstrom
Python 3.6.0

Metrics on a subset of POS tags
"""

global defaults
defaults = {'lang_col': 2,
            'POS_col': 3,
            'delimiter': '\t',
            'section_marker': 'SENT',
            'section_starts': False}


def preprocess(data, lang_col=defaults['lang_col'], POS_col=defaults['POS_col'], delimiter=defaults['delimiter'], multiple_sections=False, **marker_info):
    '''Reformats tagged data into a list of lists (... of lists, if a series of separate sections) and removes any columns not for language and POS tags. The output will place the language column first and the POS column last. If the input data is a list, it will be formatted, and the output will be a clone of it.

For multiple_sections = False:
    data as <list <str>>: list of tokens represented as strings containing the entries of each column delimited by the specified delimiter
    data as <str>: newline-delimited lines with each line representing a token and each column entry separated by the specified delimiter
    data as <list <list <str>>>: only removes/reorganizes columns
For multiple_sections = True:
    data as <list> with elements as <list <str>>, <str>, or <list <list <str>>>, corresponding to the formats above: Each element of the data is considered one section and processed as above.
    data as <str>: Data must be separated into sections; uses MARKER_INFO keywords to specify the section marker args below.
        col <int> (optional): 1-indexed column number containing section markers (default: POS_col)
        marker <str> (optional): section marker to search for (default: "{}")
        ends <bool> (optional): whether the markers indicate the ends (True, default) or starts (False) of sections

lang_col, <int>: 1-indexed column containing language tags
POS_col, <int>: 1-indexed column containing POS tags
delimiter, <str>: delimiter between each column entry within a line/token
multiple_sections, <bool>: whether to treat as multiple sections to be evaluated separately (e.g. sentences)
**marker_info: keyword arguments for splitting the data into sections (see DATA as <str> above)'''.format(defaults['section_marker'])

    if multiple_sections:
        if isinstance(data, str):
            # split sections
            col = marker_info['col'] - 1 if 'col' in marker_info else POS_col - 1
            marker = marker_info['marker'] if 'marker' in marker_info else defaults['section_marker']
            ends = marker_info['ends'] if 'ends' in marker_info else not(defaults['section_starts'])
            list_of_strings = [""] * data.count(marker)  # overestimate of number of sections; corrected later.
            section = laststart = 0
            lines = data.strip().splitlines()
            L = len(lines)
            for row, line in enumerate(lines):
                info = line.split(delimiter)
                if len(info) > col and info[col] == marker or row == L - 1:
                    if ends or row == L - 1:
                        newstart = row + 1
                    elif row == 0:
                        continue
                    else:
                        newstart = row
                    list_of_strings[section] = lines[laststart:newstart]
                    laststart = newstart
                    section += 1
            list_of_strings = list_of_strings[:section]
            return preprocess(list_of_strings, lang_col, POS_col, delimiter, True)
        else:
            for i, section in enumerate(data):
                data[i] = preprocess(section, lang_col, POS_col, delimiter)
            return data
    else:
        if isinstance(data, str):
            data = [line.split(delimiter) for line in data.strip().splitlines()]
        else:
            if isinstance(data[0], str):
                for i, line in enumerate(data):
                    data[i] = line.split(delimiter)
        maxcol = max(lang_col, POS_col)
        lang_col -= 1
        POS_col -= 1
        for line in data:
            for col in range(maxcol - len(line)):
                line.append('')
            for col in range(len(line) - 1, -1, -1):
                if col not in {lang_col, POS_col}:
                    line.pop(col)
            if lang_col > POS_col:
                line.reverse()
        return data


def preprocess_sg(data, **preprocessing):
    '''Preprocessing step for single-section functions'''

    lang_col = preprocessing['lang_col'] if 'lang_col' in preprocessing else defaults['lang_col']
    POS_col = preprocessing['POS_col'] if 'POS_col' in preprocessing else defaults['POS_col']
    delimiter = preprocessing['delimiter'] if 'delimiter' in preprocessing else defaults['delimiter']
    return preprocess(data, lang_col, POS_col, delimiter)


def preprocess_mp(data, **preprocessing):
    '''Preprocessing step for multiple-section functions'''

    lang_col = preprocessing['lang_col'] if 'lang_col' in preprocessing else defaults['lang_col']
    POS_col = preprocessing['POS_col'] if 'POS_col' in preprocessing else defaults['POS_col']
    delimiter = preprocessing['delimiter'] if 'delimiter' in preprocessing else defaults['delimiter']
    marker_info = preprocessing['marker_info'] if 'marker_info' in preprocessing else {}
    return preprocess(data, lang_col, POS_col, delimiter, True, **marker_info)


def langfrac(data, lang, tag_subset, **preprocessing):
    '''Returns the fraction of tokens from the tag subset that are of the specified language.

data, <list <list>>*: list of tokens represented as a lists of the entries of each column in the data (including language and POS tags)
    * If preprocessing, see PREPROCESS for accepted types.
lang, <str>: language of interest as named in the data
tag_subset, <set>: set of POS tags to consider, as named in the data
**preprocessing: If not empty, will preprocess; see PREPROCESS for arguments. Only works for single sections.

If no tokens from the tag subset are found, None is returned to avoid division by zero.'''

    if preprocessing:
        data = preprocess_sg(data, **preprocessing)
    subset_toks = [tok for tok in data if tok[1] in tag_subset]
    if len(subset_toks) == 0:
        return None  # avoid division by zero
    subset_toks_in_lang = [1 for tok in subset_toks if tok[0] == lang]
    return len(subset_toks_in_lang) / len(subset_toks)


def matlang(data, tag_subset, report_lang=None, **preprocessing):
    '''Returns a <set> containing the language(s) of highest frequency among tokens from the tag subset. Can also report the fraction of a specific language to conserve resources.

data, <list <list>>*: list of tokens represented as a lists of the entries of each column in the data (including language and POS tags)
    * If preprocessing, see PREPROCESS for accepted types.
tag_subset, <set>: set of POS tags considered, as named in the data
report_lang, <str>: language of interest as named in the data
**preprocessing: If not empty, will preprocess; see PREPROCESS for arguments. Only works for single sections.

If no tokens from the tag subset are found, an empty <set> is returned.'''

    if preprocessing:
        data = preprocess_sg(data, **preprocessing)
    lang_set = tuple({tok[0] for tok in data})
    N = len(lang_set)
    lang_fracs = [0] * N
    for i, lang in enumerate(lang_set):
        lang_fracs[i] = langfrac(data, lang, tag_subset)
    if None in lang_fracs:
        result = set()  # no data in the tag subset; cannot guess matrix lang
    else:
        result = {lang for i, lang in enumerate(lang_set) if lang_fracs[i] == max(lang_fracs)}

    if report_lang != None:
        frac = lang_fracs[lang_set.index(report_lang)] if report_lang in lang_set else 0
        return result, frac
    else:
        return result


def section_matlangs(data, tag_subset, report_lang=None, **preprocessing):
    '''Returns the predicted matrix language(s) of each section of the data (see MATLANG, PREPROCESSING). Use a <dict> for MARKER_INFO keywords.'''

    if preprocessing:
        data = preprocess_mp(data, **preprocessing)
    for section in data:
        yield matlang(section, tag_subset, report_lang)


def section_langfracs(data, lang, tag_subset, **preprocessing):
    '''Returns the fraction of tokens from the tag subset in each section that are of the specified language (see langfrac, PREPROCESSING). Use a <dict> for MARKER_INFO keywords.'''

    if preprocessing:
        data = preprocess_mp(data, **preprocessing)
    for section in data:
        yield langfrac(section, lang, tag_subset)


def main():
    '''argparse environment with input/output'''

    from argparse import ArgumentParser
    parser = ArgumentParser(description='Metrics on a subset of POS tags. Find the fraction of tokens constrained by the subset that are of a specific language, the predicted matrix language based on the highest fraction of tags from the subset, or either of these calculations repeatedly on a series of sections (e.g. sentences) of data.')
    parser.add_argument('input_file',
                        help='Name/Path of file with input data. Must contain language and POS tags.')
    parser.add_argument('tag_subset',
                        nargs='+',
                        help='POS tags to be considered')
    parser.add_argument('--encoding', '-e',
                        default='utf8',
                        help='Encoding type.')
    parser.add_argument('--lang_col', '-lc',
                        default=defaults['lang_col'],
                        type=int,
                        help='Column number (1-indexed) containing language tags.')
    parser.add_argument('--POS_col', '-pc',
                        default=defaults['POS_col'],
                        type=int,
                        help='Column number (1-indexed) containing POS tags.')
    parser.add_argument('--delimiter', '-d',
                        default=defaults['delimiter'],
                        help='Delimiter between columns (default: tab).')
    parser.add_argument('--single_section', '-sg',
                        action='store_true',
                        default=False,
                        help='Specify if only evaluating a single section of data (as opposed to metrics for each sentence, for example).')
    parser.add_argument('--marker_col', '-mc',
                        help='Column number (1-indexed) containing section (e.g. sentence) markers (default: POS_col).')
    parser.add_argument('--section_marker', '-um',
                        default=defaults['section_marker'],
                        help='Text in the marker column denoting a break between sections of data.')
    parser.add_argument('--section_starts', '-ss',
                        action='store_true',
                        help='Specify if section markers denote the starts of sections (ends assumed otherwise). ')
    parser.add_argument('--output_folder', '-of',
                        help='Folder in which to create the file containing output data. Not necessary for single-section metrics (will print to command line). If not specified for multiple sections, input folder assumed.')
    parser.add_argument('--language_fraction', '-lf',
                        help='Specify the language of interest (as represented in the data) here to record the fraction(s) of tokens from the tag subset present in this language.')
    parser.add_argument('--matrix_language', '-ml',
                        action='store_true',
                        help='Whether to record predicted matrix language(s)')
    args = parser.parse_args()
    if not args.marker_col:
        args.marker_col = args.POS_col
    if not(args.single_section or args.output_folder):
        args.output_folder = '\\'.join(args.input_file.split('\\')[:-1])

    print(args.tag_subset) #DEBUG
    if not(args.language_fraction or args.matrix_language):
        raise ValueError('Either langfrac or matrix_language must be specified.')

    with open(args.input_file, 'r', encoding=args.encoding) as file:
        contents = file.read().strip()

    # calculate
    if args.single_section:
        outputs = [[]]
        contents = preprocess_sg(contents, lang_col=args.lang_col, POS_col=args.POS_col, delimiter=args.delimiter)
        if args.matrix_language:
            if args.language_fraction:
                result = matlang(contents, args.tag_subset, args.language_fraction)
                for lang in result[0]:
                    outputs[0].append(lang)
                outputs[0].append(str(result[1]))
            else:
                langs = matlang(contents, args.tag_subset)
                for lang in langs:
                    outputs[0].append(lang)
        else:
            outputs.append(str(langfrac(contents, args.language_fraction, args.tag_subset)))
    else:
        outputs = [[] for i in range(contents.count('\n') + 1)]
        marker_kwargs = {'col': args.marker_col, 'marker': args.section_marker, 'ends': not(args.section_starts)}
        contents = preprocess_mp(contents, lang_col=args.lang_col, POS_col=args.POS_col, delimiter=args.delimiter, marker_info=marker_kwargs)
        if args.matrix_language:
            if args.language_fraction:
                results = section_matlangs(contents, args.tag_subset, args.language_fraction)
                nlangs = 0
                for i, result in enumerate(results):
                    langs = result[0]
                    L = len(langs)
                    if L > nlangs:
                        nlangs = L
                    for lang in langs:
                        outputs[i].append(lang)
                    outputs[i].append(str(result[1]))
                for row in outputs:
                    for i in range(nlangs + 1 - len(row)):
                        row.insert(-1, '')
            else:
                results = section_matlangs(contents, args.tag_subset)
                for i, langs in enumerate(results):
                    for lang in langs:
                        outputs[i].append(lang)
        else:
            fracs = section_langfracs(contents, args.language_fraction, args.tag_subset)
            for i, frac in enumerate(fracs):
                outputs[i].append(str(frac))

    # output
    output = '\n'.join(['\t'.join(row) for row in outputs])
    if args.output_folder:
        suffix_parts = []
        if args.matrix_language:
            suffix_parts.append('matlang')
        if args.language_fraction:
            suffix_parts.append('langfrac')
        if not args.single_section:
            for part in suffix_parts:
                part += 's'
        suffix = ' ({})'.format(' & '.join(suffix_parts))
        filename_parts = args.input_file.split('\\')[-1].split('.')
        filename_parts[-2] += suffix
        filename = '.'.join(filename_parts)
        with open('\\'.join([args.output_folder, filename]), 'w', encoding=args.encoding) as file:
            file.write(output)
    else:
        print('\n\nResults:\n' + output)

    print('\n\nDone\n\n')


if __name__ == '__main__':
    main()
