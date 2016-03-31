# igcse-paper-parser
Parses PDFs from past papers and organizes them by topic

##  Intro

This script *reads* the PDFs from past iGCSE physics exams and classifies them by topic.  
So the 2007 exam may be broken into 10 different PDFs, each one going to the corresponding directory for Forces, Waves, Radioactivity, etc.

## Strategy:

1. Read a paper and find the page numbers for each problem (see. [paperparse.py](paperparse.py)
2. Import the keywords for each category
3. Give each problem a score for each category (for example, it seems to belong to Waves (score = 3), but not to Forces (score=1))
4. Name the paper according to the chosen category and save it in the relevant directory.

We use a few simplifying assumptions:
    - A new question always starts on a new page
    - A problem will be between 1 and 3 pages long
    - a Blank page is at most 1 page long.
    - There will be at most 15 - 20 problems
    - No problem will ever be on page zero.

## Requirements

You will need pyPDF which you can install with:

```
    pip install pypdf
```

