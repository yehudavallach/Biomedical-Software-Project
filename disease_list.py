"""
Yehuda Vallach

PubMed search of a disease (particularly Alzheimer's Disease) with a list of other diseases.
Associations are printed to Excel file.
"""

import os
import wget
import shutil

DISEASE = 'alzheimer'  # choose disease
FILE = 'diseases'  # choose file name

URL = 'https://pubmed.ncbi.nlm.nih.gov/?term='


def initialize():
    """Create or remove folders and files"""
    if os.path.exists('local'):
        shutil.rmtree('local')
    os.mkdir('local')
    if os.path.exists('results.csv'):
        os.remove('results.csv')
    if os.path.exists('failed.txt'):
        os.remove('failed.txt')


def read_elements():
    """Read list of elements (plus instead of spaces)"""
    elements = []
    for line in open(FILE + '.txt', 'r'):
        elements += [line.strip()]
    return elements


def search(element, option):
    """Find number of results of a PubMed search"""
    title = element + '_' + DISEASE + '_' + option
    wget.download(URL + '"' + element + '"+' + option + '+"' + DISEASE + '"', 'local/' + title + '.html')
    os.system('find "data-results-amount" local/' + title + '.html >local/file')
    f = open('local/file', 'r')
    f.readline()
    f.readline()
    line = f.readline()
    if line == '':  # no results found
        result = '0'
    else:
        result = line.split('=')[1].replace(',', '').replace('"', '')[:-1]
    f.close()
    return result


def main():

    initialize()
    elements = read_elements()

    file_out = open('results.csv', 'a')
    file_out.write(', AND, OR, Association\n')  # print titles to Excel
    failed = open('failed.txt', 'a')

    counter = 0  # count number of elements for terminal print

    for element in elements:
        counter += 1
        try:
            and_result = search(element, 'AND')

            if and_result != '0':
                or_result = search(element, 'OR')
                association = str((int(and_result) / int(or_result)) * 100)

            else:  # no need to count or_result if and_result is zero because association is zero anyway
                or_result = '-'
                association = '0'

            file_out.write(element + ',' + and_result + ',' + or_result + ',' + association + '\n')  # print to Excel
            print('\n' + str(counter) + ': ' + element + '\nAND = %-*s OR = %s' % (
            7, and_result, or_result))  # print to terminal

        except:  # save failed elements - need to run them again
            failed.write(element + '\n')
            print('\n' + str(counter) + ': ' + element + '\nfailed')  # print to terminal
            pass

    file_out.close()
    failed.close()


if __name__ == '__main__':
    main()
