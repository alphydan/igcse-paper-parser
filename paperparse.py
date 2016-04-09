#!/usr/bin/env python

# Python imports
import subprocess

# Module imports
from pyPdf import PdfFileReader, PdfFileWriter


def start_of_pb1(page_str):
    '''
    Checks if this page has the string of problem 1.
    Returns a boolean depending on the outcome.
    '''
    if '1. ' in page_str:
        return True
    else:
        return False


def start_of_pbN(page_str, current_problem):
    '''
    Checks if this page has the string of problem N.
    Returns a boolean depending on the outcome.
    '''
    if 'BLANK PAGE' in page_str:
        return False
    else:
        current_str = '%d. ' % current_problem
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


def read_page_string(page_nr, paper_name):
    '''
    Calls a unix command to convert a single page of a PDF
    into a text file (preserving layout, without end-of-line symbol,
    with UTF-8 encoding). The output of the shell command is written
     to a text file which is read and saved.
    '''
    pdfTXT_command = "pdftotext -eol unix -nopgbrk -layout \
                     -enc UTF-8 -f %d -l %d %s temp.txt" % \
                     (page_nr, page_nr, paper_name)
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

    current_problem = 0
    pages_of_problems = {}

    for page_nr in range(1, nr_of_pages):

        page_str = read_page_string(page_nr, paper_name)

        if current_problem == 0 and start_of_pb1(page_str):
            current_problem += 1
            pages_of_problems[1] = [page_nr]
            if page_has_end(page_str):
                # Pb. 1 end on page where it starts
                current_problem += 1

        if current_problem >= 1 and start_of_pbN(page_str, current_problem):
            # current problem starts here
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

    paper.close()
    nr_of_problems = len(pages_of_problems)
    print 'This test has %s pages and %s problems' % \
          (nr_of_pages, nr_of_problems), '\n'
    return pages_of_problems


# paper_name = "papers/2004-07-3F.pdf"
# paper_name = "papers/2007-11-6H.pdf"


# xxx = paperparse(paper_name)


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
