### Student : Yousef Nademi
### Student ID: 1492308
### ccid : nademi


from os import listdir
from os.path import isfile, join
import re
import csv
import sys


# Defining possible queries

month = ['[jJ]an(?:uary)?',
         '[fF]eb(?:ruary)?',
         '[mM]ar(?:ch)?',
         '[aA]pr(?:il)?',
         '[mM]ay',
         '[jJ]un(?:e)?',
         '[jJ]ul(?:y)?',
         '[aA]ug(?:ust)?',
         '[sS]ep(?:tember)?',
         '[sS]ept',
         '[oO]ct(?:ober)?',
         '[nN]ov(?:ember)?',
         '[dD]ec(?:ember)?'
         ]

# creating OR statement between various months
months = '|'.join(month)

dayofweek = ['[mM]on(?:day)?',
             '[tT]ue(?:sday)?'
             '[wW]ed(?:nesday)?',
             '[wW]ednesday'
             '[tT]hu(?:rsday)?',
             '[fF]r(?:iday)?',
             '[sS]at(?:urday)?',
             '[sS]un(?:day)?'
             ]

# creating OR statement between dayofweek
dayofweek = '|'.join(dayofweek)


seasons = ['[fF]all',
           '[wW]inter',
           '[sS]ummer',
           '[sS]pring',
           '[aA]utumn'
           ]

# creating OR between seasons
seasons = '|'.join(seasons)
numbers = ['[oO]ne',
           '[tT]wo',
           '[tT]hree',
           '[fF]our',
           '[fF]ive',
           '[sS]ix',
           '[sS]even',
           '[eE]igth',
           '[nN]ine',
           '[tT]en',
           '1st',
           '2nd',
           '3rd'
           ]

# creating OR between numbers
numbers = '|'.join(numbers)

interval = ['[dD]ay',
            '[wW]eek',
            '[mM]onth',
            '[sS]eason',
            '[yY]ear',
            '[hH]our',
            '[mM]inute',
            '[nN]oon',
            '[tT]oday',
            '[tT]omorrow',
            '[yY]esterday'
            ]

# creating OR between interval
interval = '|'.join(interval)

deictic = ['[nN]ext',
           '[pP]rior',
           '[lL]ast',
           '[bB]efore',
           '[aA]fter',
           '[aA]go',
           '[lL]ater',
           '[fF]ew'
           ]

# creating OR between deictic
deictic = '|'.join(deictic)



def find_regex(text, file_name):
    '''
    This function compile the regular expressions to search in text,
    Input:
    - text: the text file
      file_name: Input file_name
    Output:
    - a list of cleaned regex
    '''
    temp_list = []
    pattern_list = []
    regex_list = []
    ##----------------------Pattern 1 --------------------------##
    # Appending regext pattern to regex_patterns
    regex_list.append(re.compile('\s({})\s'.format(months)))   # ('month') e.g. april-July-Aug
    pattern_list.append('month')
    ##----------------------Pattern 2 --------------------------##
    # # Find years between 1000-2039 with optional s at the end
    regex_list.append(re.compile('(\s1[0-9]{3}|20[0-3][0-9])s*'))
    # ('year') e.g. 2001, 1999, 1990s
    pattern_list.append('year')
    ##----------------------Pattern 3   ------------------------##
    regex_list.append(re.compile('((?:{})[\s-]?(?:1[0-9][0-9][0-9]|20[0-3][0-9])s*)'.format(deictic)))
    # ('relative-year') before/next... year e.g. before 1980
    pattern_list.append('relative-year')
    ##----------------------Pattern 4   ------------------------##
    regex_list.append(re.compile('(?:{})?\s*(?:{})?\s*(?:{})\s*'.format(months, deictic, interval)))
    #('month, relative-interval') eg. may last year
    pattern_list.append('month, relative-interval')
    ##----------------------Pattern 5   ------------------------##
    regex_list.append(re.compile('\s(?:{})\s'.format(dayofweek)))
    # ('dayofweek') day of the week
    pattern_list.append('dayofweek')
    ##----------------------Pattern 6 --------------------------##
    regex_list.append(re.compile('(\s?(?:1[0-9][0-9][0-9]|20[0-3][0-9])s)'))
   #('decade') e.g. 1980s, 1950s
    pattern_list.append('decade')
    ##----------------------Pattern 7 --------------------------##
    regex_list.append(re.compile('\s(?:[01]?[0-9]|2[0-9]|3[0-1])(?:\-|\s+)?(?:{})'.format(months)))
    #('day-month') eg. 1-october 2-sept  3 dec 4feb
    pattern_list.append('day-month')
    ##----------------------Pattern 8 --------------------------##
    regex_list.append(re.compile('\s(?:{})(?:\-|\s)?(?:[0-9][0-9])\s'.format(months)))
    # ('month-year') e.g dec 98
    pattern_list.append('month-year')
    ##----------------------Pattern 9 --------------------------##
    regex_list.append(re.compile('((?:[01]?[0-9]|2[0-9]|3[0-1])(?:\-|\/|\s)(?:0?[0-9]|1[012])(?:\-|\/|\s)(?:1[0-9][0-9][0-9]|20[0-3][0-9]))'))
    # ('DD(-/ )MM(-/ )YYYY') eg. 11/12/2010, 9-9-2008
    pattern_list.append('DD(-/ )MM(-/ )YYYY')
    ##----------------------Pattern 10 -------------------------##
    regex_list.append(re.compile('((?:1[0-9][0-9][0-9]|20[0-3][0-9])(?:\-|\/|\s)(?:0?[0-9]|1[012])(?:\-|\/|\s)(?:[01]?[0-9]|2[0-9]|3[0-1]))'))
    #('YYYY(-/ )MM(-/ )DD') eg. 2011/08/12
    pattern_list.append('YYYY(-/ )MM(-/ )DD')
    ##----------------------Pattern 11 -------------------------##
    regex_list.append(re.compile('((?:0?[0-9]|1[012])(?:\-|\/|\s)(?:[01]?[0-9]|2[0-9]|3[0-1])(?:\-|\/|\s)(?:1[0-9][0-9][0-9]|20[0-3][0-9]))'))
    #('MM(-/ )DD(-/ )YYYY')  # eg. 2011/08/12
    pattern_list.append('MM(-/ )DD(-/ )YYYY')
    ##----------------------Pattern 12 -------------------------##
    regex_list.append(re.compile('\s+(?:{})\s+'.format(seasons)))
    # ('season') e.g. fall, spring,..
    pattern_list.append('season')

    ##----------------------Pattern 13 -------------------------##
    regex_list.append(re.compile('((?:{0})-(?:{0}))'.format(months)))
    # ('month-month') e.g. april-July
    pattern_list.append('month-month')
    ##----------------------Pattern 14 --------------------------##
    regex_list.append(re.compile('((?:[01]?[0-9]|2[0-9]|3[0-1])(?:\-|\s*)?(?:{})(?:\-|\s*)?(?:1[0-9][0-9][0-9]|20[0-3][0-9]))'.format(months)))
    #('day-month year') eg. 1( |-)october 2014
    pattern_list.append('day-month year')
    for i, pattern in enumerate(regex_list):
        # For loop over all matches found by findall
        for m in pattern.finditer(text):
      # Appending to the list (file name, expression type, value, char_offset)
            temp_list.append([file_name, pattern_list[i], m.group(), m.start(), m.span()])
    temp_list = remove_matches(temp_list)
    return temp_list



def remove_matches(temp_list):
    '''
    This function remove matches that are copy or smaller
    take the span element of each match and put it in tuples
    '''
    tuples = [x[4] for x in temp_list]
    indexes = set()
    for j, big in enumerate(tuples):
        for i, small in enumerate(tuples):
            if(small[0]>=big[0] and small[1]<=big[1] and i!=j):
                indexes.add(i)
    for index in sorted(list(indexes), reverse=True):
        del temp_list[index]
    return temp_list


def main():
    '''
    main function where the files will be read and write
    '''
    # Path of .txt data directory
    #format in which the regex will be recorder and added to the output file
    extracted_matches = [['article_id', 'expr_type', 'value', 'char_offset', 'temp']]
    # the path where the files are
    dir_path = sys.argv[1]
    # the path that we want to write
    output_path = sys.argv[2]
    # getting the names of all files in the directory
    file_name_list = [f_name for f_name in listdir(dir_path) if isfile(join(dir_path, f_name))]
    for file_name in file_name_list:
        with open(join(dir_path, file_name)) as text_file:
            # opening one .txt file
            text = text_file.read()
            extracted_matches.extend(find_regex(text, file_name))
    ##-----------------save into CSV file-------------------------##
    # seleting the first 4 elements of each out put = dropping span() information
    extracted_matches = list(map(lambda x:x[0:4], extracted_matches))
    # Writing the output(out_list) in to a csv file(out.csv)
    with open(output_path + "output.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(extracted_matches)


if __name__ == "__main__":
    main()