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

def csv_column_reader(filepath):

	with open(filepath, 'rb') as csvfile_1:
		reader_1 = csv.reader(csvfile_1)
		column_list = reader_1.next()
	if len(column_list) != 3:
		print "<CSV FILE FORMAT ERROR> The CSV file should have three columns "
		sys.exit()
	return column_list




def csv_reader(filepath):
	'''
	CSV reader and returns the csv as a dict
	'''
	column_list = csv_column_reader(filepath)


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



def plotter(dictionary,csv_columns, pdf_file_name, color_flag, order):
	'''
	Produces a plot
	'''
	default = 0
	years = []
	papers = {}
	count = 0
	bars = []
	paper_list_for_legend = []
	if color_flag == "no":
		color = ['#d9d8d8', '#b3b2b2', '#7b7979', '#555353', '#434040', '#2e2c2c', '#1a1919', '#0d0c0c']
	elif color_flag == "yes":
		color = ['#bad4f6', '#bdb6d5', '#1259bd', '#a84bed', '#00bde4', '#cdb7b5', '#443377', '#fc4e5b', '#4c704c' ]
	else:
		print "<WRONG COLOR CODE> Please put eiter 'yes' or 'no' for color argument"
		sys.exit()

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
	for i in order:
		bars.append(plt.bar(ind,papers[i],width,bottom=y_offest,color=color[count]))
		y_offest = y_offest + papers[i]
		count = count + 1
		paper_list_for_legend.append(i)
	
	# X and Y Labels
	plt.ylabel(csv_columns[2],fontsize=20, fontstyle= 'italic')
	plt.xlabel(csv_columns[1] ,fontsize=17, fontstyle= 'italic')



	years_for_xticks = years
	if len(years_for_xticks) >= 21:
		for i in range(1,len(years_for_xticks), 2):
			years_for_xticks[i]=' '
	plt.xticks(ind + width / 2., years_for_xticks, rotation = 75,fontsize=20)
	plt.yticks(np.arange(0, max(total_number_of_papers_in_a_year) + max(total_number_of_papers_in_a_year)/5 , max(total_number_of_papers_in_a_year)/10), fontsize=19)
	plt.legend(bars, paper_list_for_legend,fontsize=12, loc='upper left')
	# plt.grid()
	plt.subplots_adjust(bottom=0.20)
	pp = PdfPages(pdf_file_name)
	plt.savefig(pp, format='pdf')
	pp.close()
	plt.show()




def argument_parser():
	'''
	Parses the argument of the 
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument("filepath")
	parser.add_argument("--pdf", default = "plot", help='Name of the pdf file')
	parser.add_argument("--order",nargs = '+', default =[])
	parser.add_argument("--color", default = "yes")
	args = parser.parse_args()
	# Storing the values in the respective variables.
	filepath = args.filepath
	pdf = args.pdf 
	order = args.order
	color = args.color
	dicti = csv_reader(filepath)
	csv_columns = csv_column_reader(filepath)
	items_in_csv = []
	for i in dicti:
		items_in_csv.append(i)
	if set(order) == set(items_in_csv) and len(items_in_csv) == len(order):
		plotter(dicti,csv_columns, pdf, color, order)
	elif len(order) == 0:
		plotter(dicti,csv_columns, pdf, color, items_in_csv)
	else:
		print "\n <ERROR> Either length of the order arguments is not 3 or they are not in the csv file"
		print "Please select the order from among the items in following list:"
		print items_in_csv
		print "\n"

if __name__ == "__main__":
	argument_parser()