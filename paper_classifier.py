#!/usr/bin/env python

# Python imports
from pyPdf import PdfFileReader, PdfFileWriter

# Module imports
from paper_parse import parse_paper_pages, write_problem2PDF
# from igcse_topics import classification


all_problems = parse_paper_pages('papers/2007-11-6-HL.pdf')
write_problem2PDF(pdf_in, pdf_out, pb_nr, pb_dictionary):
