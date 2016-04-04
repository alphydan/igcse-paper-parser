#!/usr/bin/env python
import csv
import operator

test_string = '(b) (i) State the equation which relates the acceleration of \
free fall g, gravitational potential energy, height and mass.    .............\
.............................(1)  (ii) Calculate the maximum change in \
height in metres reached by the ball. Maximum height =  ...m \
(iii) What assumption did you make to calculate the maximum height?'



def find_problem_category(pb_string):
    '''
    Takes the string parsed out of the PDF of a given problem,
    and gives a guess as to the category of the problem
    This is a very naive classifier based on a simple
    score from a keyword list.  It will return a list
    with the score and the directories to save it.
    So a return of:
    [2, 'S4 - Energy', 'S4.b - Energy transfer', 'S4.b']
    would be saved at:
    S4 - Energy/S4.b - Energy transfer/filename.Q#_S4.b.pdf
    '''

    cat = open('igcse_categories.csv', 'r',)
    cat_reader = csv.reader(cat)
    cat_headers = cat_reader.next()


    score = []
    for row in cat_reader:
        keyword_list = [row[i] for i in range(4, 11)]
        temp_score = 0
        for key in keyword_list:
            if key in pb_string:
                temp_score += 1
        directory1 = '%s - %s' % (row[1], row[0]) # S3 - Waves
        directory2 = '%s.%s - %s' % (row[1], row[2], row[3])  # S3.b - Wave Properties
        paper_name_end = '%s.%s' % (row[1], row[2])  # S3.b - Wave Properties


        score.append([temp_score, directory1, directory2, paper_name_end])

        # print keyword_list
        # print temp_score, directory1,'/',directory2, '---', paper_name_end, '\n'


    sorted_score = sorted(score, key=lambda s: s[0], reverse=True)  # sorted from top score to low score
    cat.close()
    return sorted_score[0]
