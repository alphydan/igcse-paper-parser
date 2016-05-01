#!/usr/bin/env python

# Python imports
import subprocess

# Module imports
from pyPdf import PdfFileReader, PdfFileWriter


def start_of_pb1(page_str, old_new):
    '''
    Checks if this page has the string of problem 1.
    Returns a boolean depending on the outcome.
    '''
    if old_new == 'old' and '1. ' in page_str:
        return True
    elif old_new == 'new' and '1 ' in page_str:
        return True
    else:
        return False


def start_of_pbN(page_str, current_problem, old_new):
    '''
    Checks if this page has the string of problem N.
    Returns a boolean depending on the outcome.
    '''
    if 'BLANK PAGE' in page_str:
        'it was blank'
        return False
    else:
        if old_new == 'old':
            current_str = '%d.' % current_problem
        elif old_new == 'new':
            current_str = '%d' % current_problem
        if current_str in page_str:
            return True
        else:
            return False


def page_has_end(page_str):
    '''
    Check if a problem ends here with the string
    of the total marks.
    '''
    if '(Total ' in page_str:
        return True
    else:
        return False


def read_page_string(page_nr, paper_name, old_new):
    '''
    Calls a unix command to convert a single page of a PDF
    into a text file (preserving layout, without end-of-line symbol,
    with UTF-8 encoding). The output of the shell command is written
     to a text file which is read and saved.
    '''
    if old_new == 'old':
        pdfTXT_command = "pdftotext -eol unix -nopgbrk -layout \
                         -enc UTF-8 -f %d -l %d %s temp.txt" % \
                         (page_nr, page_nr, paper_name)
    elif old_new == 'new':
        pdfTXT_command = "pdftotext -eol unix -nopgbrk \
                         -enc UTF-8 -f %d -l %d %s temp.txt" % \
                         (page_nr, page_nr, paper_name)

    # The old/new branches are created for some reason I don't understand
    # when using -layout, some recent papers lose the
    # "Total for Question N" string so I decided to create a branch without it.

    subprocess.call(pdfTXT_command, shell=True)
    a_page = open("temp.txt", 'rb')
    page_str = a_page.read()
    a_page.close()
    return page_str


def paperparse(paper_name):
    '''
    calls pyPDF.
    ``input: paper-name (opens a PDF file)
    ``output: dictionary of problems and pages
    output example: {1:[4,5], 2: [6], 3: [7,8]}
    which would be read:
    - problem 1 is on pages 4 and 5
    - problem 2 is on page 6
    - problem 3 is on pages 7 and 8, etc
    '''
    paper = open(paper_name, 'rb')
    pdf = PdfFileReader(paper)
    nr_of_pages = pdf.getNumPages()

    paper_year = paper_name.split('/')[1].split('-')[0]
    if int(paper_year) >= 2011:
        old_new = 'new'  # format of problem nr is: '1   '
    else:
        old_new = 'old'  # format of problem nr is: '1. '


    current_problem = 0
    pages_of_problems = {}

    for page_nr in range(3, nr_of_pages):
        current_found = 0
        page_str = read_page_string(page_nr, paper_name, old_new)

        if current_problem == 0 and start_of_pb1(page_str, old_new):
            'start of 1 found'
            current_problem += 1
            pages_of_problems[1] = [page_nr]

            if page_has_end(page_str):
                # Pb. 1 end on page where it starts
                current_problem += 1
                continue # increment a page and skip ifs below


        if pages_of_problems.get(current_problem):
            # we already have a starting page for this problem
            current_found = 1

            if current_problem == 1 and page_has_end(page_str):
                pages_of_problems[current_problem].append(page_nr)
                current_problem += 1
                continue # move on to problem 2

        # print page_str
        if current_problem > 1 and \
                start_of_pbN(page_str, current_problem, old_new):

            # current problem starts here
            if current_found:
                pages_of_problems[current_problem].append(page_nr)
            else:
                pages_of_problems[current_problem] = [page_nr]
            if page_has_end(page_str):
                # ends on the page it starts
                current_problem += 1  # move to next problem


        if pages_of_problems.get(current_problem):
            # we already have a starting page for this problem
            # but it didn't end on that same page
            if page_has_end(page_str):
                pages_of_problems[current_problem].append(page_nr)
                current_problem += 1
            else:
                pass
                # print current_problem, 'no end', page_nr


    paper.close()
    nr_of_problems = len(pages_of_problems)
    print 'This test has %s pages and %s problems' % \
          (nr_of_pages, nr_of_problems), '\n'

    # did we miss any 3 page problems?
    full_pages_of_problems = pages_of_problems
    for pb in pages_of_problems:
        if len(pages_of_problems[pb]) > 1:
             full_pages_of_problems[pb] = range(pages_of_problems[pb][0], pages_of_problems[pb][1]+1)

    # print full_pages_of_problems
    return full_pages_of_problems


def write_problem2PDF(pdf_in, pdf_out, page_list):
    '''
    Takes a PDF and outputs one with just the selected pages
    from a selected problem
    '''
    f = open(pdf_in, 'rb')
    pdf = PdfFileReader(f)

    output = PdfFileWriter()

    for pb_pg in page_list:
        output.addPage(pdf.getPage(pb_pg-1))
    # finally, write "output" to document-output.pdf
    outputStream = file(pdf_out, "wb")
    output.write(outputStream)
    print 'pages %s from PDF %s have been printed to %s' % \
          (page_list, pdf_in, pdf_out)
    return None


def get_problem_string(paper_name, page_list):
    '''
    This function opens a PDF and returns the string
    corresponding to the given page list.
    '''

    f = open(paper_name, 'rb')
    pdf = PdfFileReader(f)

    problem_string = ''
    for pg in page_list:
        contents = str(pdf.getPage(pg-1).extractText().encode('ascii', 'ignore'))
        problem_string += contents

    return problem_string


# paper_name = "papers/2007-11-6H.pdf"
# paper_name = "papers/2011-06-1P.pdf"

# paper_name = "papers/2015-06-1P.pdf"

# xxx = paperparse(paper_name)
# print xxx
