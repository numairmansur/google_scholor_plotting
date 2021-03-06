'''
@author: numair mansur (numair.mansur@gmail.com)

Research Group on Learning, Optimization,
and Automated Algorithm Design
University of Freiburg, Germany.
'''
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import os
import argparse
import seaborn as sns
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



def plotter(dictionary,csv_columns, pdf_file_name, color_flag, order,y_max,y_increment):
	'''
	Produces a plot
	'''
	sns.set(style="white", color_codes=True, font_scale=1.2)
	sns.set_style("ticks", {"xtick.major.size": 3, "ytick.major.size": 2})


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
	plt.ylabel(csv_columns[2],fontsize=22, fontstyle= 'italic')
	plt.xlabel(csv_columns[1] ,fontsize=22, fontstyle= 'italic')



	years_for_xticks = years
	if len(years_for_xticks) >= 21:
		for i in range(1,len(years_for_xticks), 2):
			years_for_xticks[i]=' '
	
	#X and Y Ticks 
	plt.xticks(ind + width / 2., years_for_xticks, rotation = 75,fontsize=20)
	plt.yticks(np.arange(0, max(total_number_of_papers_in_a_year) + max(total_number_of_papers_in_a_year)/5 if y_max == None else int(y_max)+1,
		int(y_increment)),
		fontsize=19)

	#Reverse the legend order
	bars= list(reversed(bars))
	paper_list_for_legend = list(reversed(paper_list_for_legend))

	plt.legend(bars, paper_list_for_legend,fontsize=12, loc='upper left')
	plt.subplots_adjust(bottom=0.20)
	pp = PdfPages(pdf_file_name)
	plt.savefig(pp, format='pdf')
	pp.close()
	return plt

def bar_plot(x, curves, title="", width=0.15,
            colors=['b', 'g', 'r', 'c', 'm', 'y', 'k'], legend=True,
            x_title="Year", y_title="# citations",bar_names = [],color="yes", pdf_file_name="default"):
    # Set Appearance properties using Seaborn
    sns.set(style="white", color_codes=True, font_scale=1.2)
    sns.set_style("ticks", {"xtick.major.size": 3, "ytick.major.size": 2})
    #sns.set_titles(col_template = "{col_name}", fontweight = 'bold', size = 18)
    # - - - - - - - -- - - - - - - - -
    if color == "yes":
    	colors=['b', 'g', 'r', 'c', 'm', 'y', 'k']
    else:
    	colors = ['#d9d8d8', '#b3b2b2', '#7b7979', '#555353', '#434040', '#2e2c2c', '#1a1919', '#0d0c0c']
    x = x.astype(float)
    fig, ax = plt.subplots()
    bars = []
    # Stores the information about how many bars are saved on a X-Location.
    x_location_map = dict()

    # Pre-Process and adjust X-axis location data
    for i, j in enumerate(x):
        for l, k in enumerate(j):
            if k in x_location_map:
                x[i][l] = x[i][l] + (x_location_map[k] * width)
                x_location_map[k] += 1
            else:
                x_location_map[k] = 1
    # - - - - - - - - - - - - -
    for i, j in enumerate(x):
        bar = ax.bar(
            j,
            curves[i][0],
            width,
            yerr=curves[i][1],
            color=colors[i],
            error_kw=dict(
                ecolor='#525252',
                capsize=0,
                capthick=0))
        bars.append(bar)

    bars = list(reversed(bars))
    bar_names = list(reversed(bar_names))
    ax.set_ylabel(y_title, fontsize=14)
    ax.set_xlabel(x_title, fontsize=14)
    ax.set_title(title, fontsize=15)
    ax.set_xticks([i + ((x_location_map[i] * width) / 2)
                   for i in x_location_map])
    ax.set_xticklabels([int(i) for i in x_location_map])
    if legend:
    	ax.legend(bars, bar_names, loc=0)
	pp = PdfPages(pdf_file_name)
    plt.savefig(pp, format='pdf')
    pp.close()
    return plt


def main():
	'''
	Parses the argument of the 
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument("filepath")
	parser.add_argument("--pdf", default = "plot", help='Name of the pdf file')
	parser.add_argument("--order",nargs = '+', default =[])
	parser.add_argument("--color", default = "yes")
	parser.add_argument("--y_max", default = None)
	parser.add_argument("--y_increment", default=50)
	args = parser.parse_args()
	# Storing the values in the respective variables.
	filepath = args.filepath
	pdf = args.pdf 
	order = args.order
	color = args.color
	y_max = args.y_max
	y_increment = args.y_increment

	dicti = csv_reader(filepath)
	csv_columns = csv_column_reader(filepath)
	items_in_csv = []
	for i in dicti:
		items_in_csv.append(i)
	if set(order) == set(items_in_csv) and len(items_in_csv) == len(order):
		plot =plotter(dicti,csv_columns, pdf, color, order,y_max,y_increment)
	elif len(order) == 0:
		plot =plotter(dicti,csv_columns, pdf, color, items_in_csv,y_max,y_increment)
	else:
		print "\n <ERROR> Either length of the order arguments is not 3 or they are not in the csv file"
		print "Please select the order from among the items in following list:"
		print items_in_csv
		print "\n"

	#The other curve.
	x=[]
	curves = []
	bar_names=[]
	for i in dicti:
		bar_names.append(i)
		x_axis = [int(j) for j in dicti[i]]
		x_axis.sort()
		curve = []
		for j in x_axis:
			curve.append(dicti[i][str(j)])
		curves.append(np.array([curve,[0 for i in curve]]))
		x.append(x_axis)

	x=np.array(x,dtype=object)
	plot = bar_plot(x, curves, legend = True,bar_names=bar_names,color=color,pdf_file_name = pdf+"2")
	plot.show()



if __name__ == "__main__":
	main()