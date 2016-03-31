#!/usr/bin/env python
from pyPdf import PdfFileReader, PdfFileWriter


def last_page(current_problem, contents):
    '''
    short function to check if the problem
    ends on this page.  Question N ends here if the string
    "QN(Total" is found on the page.
    '''
    end_of_question_string = 'Q%d(Total' % current_problem
    if end_of_question_string in contents[0]:
        return True
    else:
        return False


def parse_paper_pages(paper_name):
    '''
    This function opens a PDF and finds which pages
    correspond to each problem returning a dictionary
    with that information:
    input: PDF name
    output: {1:[4,5], 2: [6], 3: [7,8]}
    which would be read:
    - problem 1 is on pages 4 and 5
    - problem 2 is on page 6
    - problem 3 is on pages 7 and 8, etc
    '''

    f = open(paper_name, 'rb')
    pdf = PdfFileReader(f)
    nr_of_pages = pdf.getNumPages()

    # empty list of problems and pages:
    pages_of_problems = {}
    for i in range(1, 21):
        pages_of_problems[i] = [0]

    current_problem = 0

    for pg in range(0, nr_of_pages):

        contents = pdf.getPage(pg).extractText().split('\n')

        # Does this page contain Q1?
        if (current_problem == 0) and (' 1.' in contents[0]):
            print 'p.', pg+1, ' -> start of question 1'
            current_problem = 1  # Q1 found. Disregard next '1.' strings
            pages_of_problems[1][0] = pg

        # Have we found page 1 of the current problem?
        if current_problem >= 1 and pages_of_problems[current_problem][0] == 0:
            # if it's a blank page it won't be the start of a new problem
            if 'BLANK PAGE' in contents[0]:
                pass

            # if it's not a blank page, then a new problem must be starting
            else:
                pages_of_problems[current_problem][0] = pg
                # was this first page also the last page?
                if last_page(current_problem, contents):
                    current_problem += 1

        elif current_problem >= 1:
            # We have the first page, but not the last one
            if last_page(current_problem, contents):
                # if it's the last page, move on to next problem
                pages_of_problems[current_problem].append(pg)
                current_problem += 1

            elif current_problem > 1:
                pages_of_problems[current_problem].append(pg)

    # Clean up empty problems:
    all_problems = {i: pages_of_problems[i] for i in pages_of_problems
                    if pages_of_problems[i][0] != 0}

    nr_of_problems = len(all_problems)
    print 'This test has %s pages and %s problems' % (nr_of_pages, nr_of_problems)

    f.close()
    return all_problems




def write_problem2PDF(pdf_in, pdf_out, pb_nr, pb_dictionary):
    '''
    Takes a PDF and outputs one with just the selected pages
    from a selected problem
    '''
    f = open(pdf_in, 'rb')
    pdf = PdfFileReader(f)

    output = PdfFileWriter()

    pb_pg_list = pb_dictionary[pb_nr]
    for pb_pg in pb_pg_list:
        output.addPage(pdf_in.getPage(pg_pg))
    # finally, write "output" to document-output.pdf
    outputStream = file(pdf_out, "wb")
    output.write(outputStream)
    print 'pages %s from PDF %s have been printed to %s' % (pb_pg_list, pdf_in, pdf_out)
    return None
