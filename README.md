# igcse-paper-parser
Parses PDFs from past papers and organizes them by topic

##  Intro

This script *reads* the PDFs from past iGCSE physics exams and classifies them by topic.  
So the 2007 exam may be broken into 10 different PDFs, each one going to the corresponding directory for Forces, Waves, Radioactivity, etc.

## Strategy:

1. Read a paper and find the page numbers for each problem (cf. [paperparse.py](paperparse.py) )
2. Import the keywords for each category (cf. [igcse_categories.csv](igcse_categories.csv))
3. Give each problem a score for each category (for example, it seems to belong to Waves (score = 3), but not to Forces (score=1)) (cf. [problem_classifier.py](problem_classifier.py))
4. Name the paper according to the chosen category and save it in the relevant directory (cf. [paper_classifier.py](paper_classifier.py))

We use a few simplifying assumptions:

    - A new question always starts on a new page
    - A problem will be between 1 and 3 pages long
    - a Blank page is at most 1 page long.
    - No problem will ever be on page zero.

## Requirements

You will need [`python`](https://www.python.org/) and pyPDF which you can install with:

```
    pip install pyPDF
```

This script also uses the linux command line utility `pdftotext` which can be installed on [mac](http://superuser.com/questions/56272/is-the-pdftotext-command-line-tool-for-mac) and [windows](http://www.foolabs.com/xpdf/download.html)
