'''
author: Muhammad Numair Mansur (numair.mansur@gmail.com)
University of Freiburg, Germany
'''
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import os
import argparse
from matplotlib.backends.backend_pdf import PdfPages
def csv_reader(filepath):
    '''
    CSV reader and returns the csv as a dict
    '''
    with open(filepath, 'rb') as csvfile_1:
    	reader_1 = csv.reader(csvfile_1)
    	column_list = reader_1.next()
    if len(column_list) !=3:
    	print "<CSV FILE FORMAT ERROR> The CSV file should have three columns "
    	sys.exit()
    with open(filepath, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        result = {}
        papers = []
        
        first_column = column_list[0]
        second_column = column_list[1]
        third_column = column_list[2]

        for row in reader:
            if row[first_column] not in papers:
                result[row[first_column]] = {}
                papers.append(row[first_column])
            result[row[first_column]][row[second_column]] = int(row[third_column])
    return result


def plotter(dictionary,pdf_file_name):
    '''
    Produces a plot
    '''
    default = 0
    years = []
    papers = {}
    count = 0
    color = ['#d9d8d8', '#b3b2b2', '#7b7979', '#555353', '#434040', '#2e2c2c', '#1a1919', '#0d0c0c']
    bars = []
    paper_list_for_legend = []
    for rows in dictionary:
        for year in dictionary[rows]:
            if year not in years:
                years.append(year)
        papers[rows] = []
    years = sorted(years)

    for i in years:
        for j in papers:
            papers[j].append(dictionary[j].setdefault(i, default))
    


    # Find the total number of papers in a year
    total_number_of_papers_in_a_year =[0] * len(years)
    for i in papers:
        total_number_of_papers_in_a_year = map(sum, zip(papers[i],total_number_of_papers_in_a_year))

    N = len(years)
    ind = np.arange(2,N+2)
    width = 0.75 # width of the bars
    y_offest = np.array([0.0] * len(years))
    for i in papers:
        bars.append(plt.bar(ind,papers[i],width,bottom=y_offest,color=color[count]))
        y_offest = y_offest + papers[i]
        count = count + 1
        paper_list_for_legend.append(i)
    # plt.ylabel('Number of Citations',fontsize=20, fontstyle= 'italic')
    # plt.xlabel('Year',fontsize=15, fontstyle= 'italic')



    years_for_xticks = years
    if len(years_for_xticks) >= 21:
        for i in range(1,len(years_for_xticks), 2):
            years_for_xticks[i]=' '
    print max(total_number_of_papers_in_a_year) + max(total_number_of_papers_in_a_year)/5
    plt.xticks(ind + width / 2., years_for_xticks, rotation = 75,fontsize=20)
    plt.yticks(np.arange(0, max(total_number_of_papers_in_a_year) + max(total_number_of_papers_in_a_year)/5 , max(total_number_of_papers_in_a_year)/10), fontsize=20)
    plt.legend(bars, paper_list_for_legend,fontsize=12, loc='upper left')
    # plt.grid()
    plt.subplots_adjust(bottom=0.15)
    pp = PdfPages(pdf_file_name)
    plt.savefig(pp, format='pdf')
    pp.close()
    # plt.show()
    print "SHOWING THE PLOT NOW"



def argument_parser():
	'''
	Parses the argument of the 
	'''
	print "Entered the argument parser"
	parser = argparse.ArgumentParser()
	parser.add_argument("filename")
	parser.add_argument("--pdf", default = "plot", help='Name of the pdf file')
	parser.add_argument("--order",nargs ='+', default =[])
	parser.add_argument("--color", default="no")
	args = parser.parse_args()
	# Storing the values in the respective variables.
	filename = args.filename
	pdf = args.pdf 
	order = args.order
	color = args.color
	dicti = csv_reader(filename)
	print order
    print order
	return 0


if __name__ == "__main__":
    argument_parser()
    
