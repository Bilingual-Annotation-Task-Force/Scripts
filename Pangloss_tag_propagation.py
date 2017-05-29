"""
Eric Nordstrom
5/24/2017
Python 3.6.0

For filling in gaps in the Pangloss TSV data. Locates and attempts to fix errors in all TSV files in INFOLDER, then writes the updated data to OUTFOLDER. Neither folder should contain other TSV files.

Does not use ARGPARSE.

Command line inputs:
    1:  input folder containing original TSV data
    2:  output folder to hold tag-propagated TSV data
    3:  [OPTIONAL] encoding type (UTF-8 assumed if nothing specified)
    4:  [OPTIONAL] custom file ending ("(TP)" if nothing specified)
"""


"""Define Methods"""

def TSVs( folder ):
    '''Returns a list of all filenames ending with '.tsv' within the specified folder directory'''

    import os
    
    for root, dirs, files in os.walk(folder):
        pass
    
    file_list = list(files) #to prevent skipping consecutive non-TSV files

    for file in file_list:
        if not file.endswith('.tsv'):
            files.remove(file)

    return files

def try_fix():
    '''Updates variables LINE (and thereby CONTENT) and MATCH; requires variables INFOLDER, OUTFOLDER, ENC, INFILES, FILENUM, CONTENT, LINE, ROW, and COL to be specified ahead of time'''
    
    global line, match

    search_filenum = 0 #order is: current file (search_filenum = 0), then OUTFOLDER files (1 <= search_filenum <= filenum), then remaining INFOLDER files (search_filenum > filenum)
    search_row = 0
    match = False
    search_content = content

    if col == 0: #Token
        def condition():
            return line[2:4] == search_line[2:4] and search_line[0] != ''
    elif col == 1: #Sentence
        line[1] = content[row-1].split('\t')[1] #simply assume sentence is same as for previous token
        match = True
    else: #Translation or Language
        def condition():
            return line[0] == search_line[0] and search_line[col] != ''

    while not match and search_filenum < len(infiles):
        
        search_line = search_content[search_row].split('\t')
        entry = search_line[col]
        
        if condition():
            line[col] = entry
            match = True
            
        else:
        
            search_row += 1

            if search_row == len(search_content):

                search_filenum += 1
                search_row = 0

                if search_filenum <= filenum:
                    folder = OUTFOLDER
                    search_filename = in_to_out( infiles[search_filenum-1] )
                elif search_filenum < len(infiles):
                    folder = INFOLDER
                    search_filename = infiles[search_filenum]
                else:
                    continue                            
                
                search_content = open( '%s\\%s' % ( folder, search_filename ), encoding = ENC ).read().splitlines()

def in_to_out( filename ):
    if filename.endswith( ' %s.tsv' % new_ending ):
        return filename
    else:
        return '%s %s.tsv' % ( filename[:-4], new_ending )

def write_outfile():
    '''Writes updated data to OUTFILE; reqires OUTFOLDER, ENC, CONTENT, LINE, INFILENAME, and ROUND (and i if ROUND > 0) to be specified ahead of time'''
    
    output = content[0]
    for line in content[1:]:
        output += '\n' + line

    if Round:
        first_part = 'Fixed error %s' % ( i + 1 )
    else:
        first_part = 'Tag-propagated "%s"' % infilename

    outfilename = in_to_out(infilename)
    print( '%s. Writing to "%s"...' % ( first_part, outfilename ) )
    outfile = open( '%s\\%s' % ( OUTFOLDER, outfilename ), 'w', encoding=ENC )
    outfile.write(output)
    outfile.close()
    print('File saved.')

def get_answer(prompt, accepted_answers, answer_type = str):
    '''Loops until input is an accepted answer'''

    answer = 'a;sdlfkj'*100

    while answer not in accepted_answers:
        answer = answer_type( input( prompt ) )
        if answer.lower() not in accepted_answers:
            print( '"%s" is not an accepted response.' % str( answer ) )

    return answer


"""Set up""" #can improve with ARGPARSE

import sys

argv = sys.argv

INFOLDER = argv[1]
OUTFOLDER = argv[2]

if len(argv) > 3:
    ENC = argv[3]
else:
    ENC = 'utf8'

if len(argv) > 4:
    new_ending = argv[4]
else:
    new_ending = '(TP)'

infiles = TSVs( INFOLDER )
Round = 0


"""Perform main tag propagation"""

errors = [] #list of dicts of error info
res = [] #list of error resolution statuses
unres = 0 #number of unresolved errors

for filenum in range(0,len(infiles)):
    
    infilename = infiles[filenum]
    content = open( '%s\\%s' % ( INFOLDER, infilename ), encoding=ENC ).read().splitlines()               
    print( '\nBeginning tag propagation for "%s"...' % infilename )
        
    for row in range(0,len(content)):

        line = content[row].split('\t')
        
        for col in range(0,4):

            if line[col] == '': #fill in missing data

                try_fix()

                if match:
                    status = 'Resolved'
                    res.append(True)
                else:
                    status = 'Unresolved'
                    res.append(False)
                    unres += 1

                errors.append( {'file':infilename,'row':row,'col':col,'status':status} )
    
    write_outfile()


"""Try fixing remaining errors with updated data""" #can be made less expensive/sloppy. can also be made optional.

INFOLDER = OUTFOLDER
infiles = TSVs( OUTFOLDER )

last_state = [True]*len(res)

while res != last_state:
    
    Round += 1
    last_state = res
    
    print( '\nCompleted round %s of tag propagation. Resolved %s of %s errors. Retrying remaining %s errors with updated data...\n' % ( Round, len(res) - unres, len(res), unres ) )
    
    for i in range(0,len(res)):
        if not res[i]:
            
            error = errors[i]
            infilename, row, col = error['file'], error['row'], error['col']
            
            outfilename = in_to_out(infilename)
            content = open( '%s\\%s' % ( OUTFOLDER, outfilename ), encoding=ENC ).read().splitlines()
            line = content[row].split('\t')
            filenum = infiles.index(outfilename)

            try_fix()

            if match:
                write_outfile()
                error['status'] = 'Resolved'
                res[i] = True
                unres -= 1
            else:
                print( 'Failed to fix error %s.' % ( i + 1 ) )


"""Summarize & end"""

print( '\nTag propagation complete. All possible corrections made. Resolved %s of %s errors.' % ( len(res) - unres, len(res) ) )
prompt = '\nDisplay errors? ( "A" = all, "U" = unresolved, "N" = none/exit )\nInput: '
accepted_answers = {'a','u','n'}
display = get_answer( prompt, accepted_answers )

if display == 'a':
    for i in range(0,len(res)):
        print( 'Error %s: %s' % ( i+1, errors[i]) )
elif display == 'u':
    for i in range(0,len(res)):
        if not res[i]:
            print( 'Error %s: %s' % ( i+1, errors[i]) )

prompt = '\nDisplay resolutions? (Y/N): '
accepted_answers = {'y','n'}
display = get_answer( prompt, accepted_answers )

if display == 'y':
    for i in range(0,len(res)):
        if res[i]:
            error = errors[i]
            infilename, row, col = error['file'], error['row'], error['col']
            outfilename = in_to_out(infilename)
            resolution = open( '%s\\%s' % ( OUTFOLDER, outfilename ), encoding=ENC ).read().splitlines()[row].split('\t')[col]
            print( 'Error %s (col %s): %s' % ( i+1, col+1, resolution ) )

print('\nDone.')
