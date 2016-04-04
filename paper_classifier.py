#!/usr/bin/env python

# Python imports
import csv
import os

# Module imports
from pyPdf import PdfFileReader, PdfFileWriter

# Local Imports
from paperparse import parse_paper_pages, get_problem_string, write_problem2PDF
from problem_classifier import find_problem_category
# from igcse_topics import classification


# Get list of papers
path = 'papers/'
list_of_papers = sorted(os.listdir(path))


print list_of_papers
print list_of_papers[0], '\n\n'

paper_name = 'papers/%s' % list_of_papers[0]
root_paper_name = paper_name.split('/')[1].split('.pdf')[0]


all_problems = parse_paper_pages(paper_name, verbose=True)

print all_problems

for pb_nr in all_problems:
    print pb_nr


pb_nr = 1

paper_string = get_problem_string(paper_name, all_problems[pb_nr])

pb_cat = find_problem_category(paper_string)
pdf_out = 'paper_problems/%s/%s/%s.Q%d_%s.pdf' % (pb_cat[1], pb_cat[2], root_paper_name, pb_nr, pb_cat[3])

print pb_cat
print pdf_out


# write_problem2PDF(paper_name, pdf_out, all_problems[pb_nr])
