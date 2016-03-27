#!/usr/bin/env python
from pyPdf import PdfFileReader, PdfFileWriter
from igcse_topics import classification

'''
######  Strategy of this program:  ######

The idea is to read a PDF page by page.
We identify where a question begins and where a question ends.
We then print the one, two or three pages containing the question to another file.
(we read and split the PDF with "pyPdf")

We can use a few simplifying assumptions:
    - A new question always starts on a new page
    - A problem will be between 1 and 3 pages long
    - a Blank page is at most 1 page long.
    - There will be at most 15 - 20 problems
    - No problem will ever be on page zero.
'''

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


f = open('2007-11-6-HL.pdf', 'rb')
pdf = PdfFileReader(f)
nr_of_pages = pdf.getNumPages()


# empty list of problems and pages:
pages_of_problems = {}
for i in range(1,21):
    pages_of_problems[i] = [0]

current_problem = 0
print '##################--------------------#################'
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

    elif current_problem >=1:
        # We have the first page, but not the last one
        if last_page(current_problem, contents):
            # if it's the last page, move on to next problem
            pages_of_problems[current_problem].append(pg)
            current_problem +=1

        elif current_problem >1:
            pages_of_problems[current_problem].append(pg)



# Clean up empty problems:
all_problems = {i:pages_of_problems[i] for i in pages_of_problems \
if pages_of_problems[i][0]!=0}

nr_of_problems = len(all_problems)
print 'This test has %s pages and %s problems' % (nr_of_pages, nr_of_problems)


for pb in all_problems:
    output = PdfFileWriter()
    for pb_pg in all_problems[pb]:
        output.addPage(pdf.getPage(pb_pg))
    pdf_name = '2007-11-6-HL.Q%s.pdf' % pb
    # finally, write "output" to document-output.pdf
    outputStream = file(pdf_name, "wb")
    output.write(outputStream)


f.close()

