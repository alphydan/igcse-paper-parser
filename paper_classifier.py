#!/usr/bin/env python

# Python imports
import csv
import os

# Module imports
from pyPdf import PdfFileReader, PdfFileWriter

# Local Imports
from paperparse import paperparse, write_problem2PDF, get_problem_string
from problem_classifier import find_problem_category
# from igcse_topics import classification


# Get list of papers
path = 'papers/'
list_of_papers = sorted(os.listdir(path))



def split_paper(paper_name):
    root_paper_name = paper_name.split('/')[1].split('.pdf')[0]
    all_problems = paperparse(paper_name)
    print root_paper_name, '--->', all_problems, '\n\n'

    for pb_nr in range(1, len(all_problems)+1):
        print pb_nr
        paper_string = get_problem_string(paper_name, all_problems[pb_nr])
        pb_cat = find_problem_category(paper_string)
        pdf_out = 'paper_problems/%s/%s/%s.Q%d_%s.pdf' % \
            (pb_cat[1], pb_cat[2], root_paper_name, pb_nr, pb_cat[3])
        print pdf_out
        write_problem2PDF(paper_name, pdf_out, all_problems[pb_nr])


print list_of_papers, '\n\n'
print len(list_of_papers)

for paper_nr in range(1, len(list_of_papers)):
    paper_name = 'papers/%s' % list_of_papers[paper_nr]
    print paper_name
    split_paper(paper_name)

# split_paper('papers/2010-06-2H.pdf')
