# igcse-paper-parser
Parses PDFs from past papers and organizes them by topic

##  Strategy

The idea is to read a PDF page by page.  We identify where a question begins and where a question ends.
We then print the one, two or three pages containing the question to another file. (we read and split the PDF with "pyPdf")

We use a few simplifying assumptions:
    - A new question always starts on a new page
    - A problem will be between 1 and 3 pages long
    - a Blank page is at most 1 page long.
    - There will be at most 15 - 20 problems
    - No problem will ever be on page zero.
