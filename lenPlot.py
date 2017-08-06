import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np



def lenArray(contig_dict):
	"""
	contig_dict: a dictionary object from ContigLen()
	
	returns a plot showing the distribution of the contigs
	"""
	
	length = []
	
	for v in contig_dict.values():
		
		length.append(v)
	
	length.sort()
		
	length_array = np.array(length)
	
	
	return length_array


def lenDistPlot(len1, len2, col1, col2, lab1, lab2, savefig):
	"""
	len1: numpy array
	len2: numpy array
	
	draws a distribution plot
	"""
	
	bins = [200, 1200, 2200, 3200, 4200, 5200, 6200, 7200, 8200, 9200]
	labels = np.array(['200-1200', '1201-2200', '2201-3200',
				'3201-4200', '4201-5200', '5201-6200', '6201-7200','7201-8200', '> 8201'])

	index = np.arange(len(bins) - 1)
	
	
	# cut the bin range
	cuts1 = pd.cut(len1, bins = bins, labels = labels).value_counts() / len(len1)
	cuts2 = pd.cut(len2, bins = bins, labels = labels).value_counts() / len(len2)
	# bar plot	
	bar_width = 0.35
	fig, ax = plt.subplots()
	ax.tick_params(direction = 'out', pad = 0.5) # set the direction of ticks facing out
	ax.spines['right'].set_visible(False) # remove right axis
 	ax.spines['top'].set_visible(False) # remove top axis
	ax.xaxis.set_ticks_position('bottom')
	ax.yaxis.set_ticks_position('left')
	
	r1 = plt.bar(index, cuts1, bar_width, alpha = 0.5, color = col1, edgecolor = 'none', label = lab1)
	r2 = plt.bar(index + bar_width, cuts2, bar_width, alpha = 0.5, color = col2, edgecolor = 'none',label = lab2)
	plt.margins(x = 0.01) # so the first bar wont touch y axis
	plt.xticks(index + bar_width, labels, rotation = 60)
	plt.xlabel('Contig Length (bp)')
	plt.ylabel('Frequency (%)')
	#plt.title('Distribution of contig length')
	
	# set legend, no frame	
	plt.legend(frameon = False)
	
	
	if savefig == True:
		plt.savefig('Contig_length_distr' + '.png', dpi = 200, bbox_inches = 'tight')

	plt.show()

sum(orig)
pros = lenArray(proc_contig_dict)
orig = lenArray(orig_contig_dict)


lenDistPlot(len1 = pros, len2 = orig, col1 = 'b', col2 = 'g', lab1 = 'Processed Assembly', lab2 = 'Original Assembly', savefig = True)