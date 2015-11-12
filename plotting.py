'''
author: Muhammad Numair Mansur (numair.mansur@gmail.com)
University of Freiburg, Germany
'''
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import os
from matplotlib.backends.backend_pdf import PdfPages
def csv_reader(filepath):
    '''
    CSV reader and returns the csv as a dict
    '''
    with open(filepath, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        result = {}
        papers = []
        for row in reader:
            if row['paper'] not in papers:
                result[row['paper']] = {}
                papers.append(row['paper'])
            result[row['paper']][row['year']] = int(row['citations'])
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
    plt.xticks(ind + width / 2., years_for_xticks, rotation = 75,fontsize=20)
    plt.yticks(np.arange(0, max(total_number_of_papers_in_a_year) + max(total_number_of_papers_in_a_year)/10 , max(total_number_of_papers_in_a_year)/10), fontsize=20)
    plt.legend(bars, paper_list_for_legend,fontsize=12, loc='upper left')
    # plt.grid()
    plt.subplots_adjust(bottom=0.15)
    pp = PdfPages(pdf_file_name)
    plt.savefig(pp, format='pdf')
    pp.close()
    plt.show()
    return plt

def main():
    '''
    The main method
    '''
    if len(sys.argv) == 2:
    	file_name = sys.argv[1]
    	dicti = csv_reader(file_name)
    	plotter(dicti,'plot.pdf')
    elif len(sys.argv) == 4 and sys.argv[2] == '--pdf':
    	file_name = sys.argv[1]
    	pdf_file_name = sys.argv[3]
    	dicti = csv_reader(file_name)
    	plotter(dicti,pdf_file_name+'.pdf')
    else:
    	print('\n Usage: python plotting.py <.csv file> --pdf [name_of_the_pdf_file] \n ')
        sys.exit()



if __name__ == "__main__":
    main()
