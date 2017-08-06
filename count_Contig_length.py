def ContigLen(filename):
	"""
	filename: a fasta file name
	
	returns a list of tuples (transcript id, length)
	"""
	
	fh = open(filename, 'r')

	contigs = {}
	
	for line in fh:
		
		line = line.strip()
		
		if line.startswith('>'):
			name = line.split('>')[1]
			contigs[name] = ''
		else:
			contigs[name] += line
			
	len_contigs_dict = {x:len(y) for x, y in contigs.items()}
	len_contigs_tuple = [(len(y), x) for x, y in contigs.items()]
	
	len_contigs_tuple.sort()

	return len_contigs_tuple, len_contigs_dict		
			
def FreqLen(contig_list, bp):
	"""
	contig_list: a list contains tuples with length information
	bp: an integer, the contig length you want to count
	
	returns a percentage of the length in total number
	"""
	assert type(bp) == int, 'bp must be an integer'
	
	count = 0
	for i in contig_list:
		
		if i[0] < bp:
			count += 1
			
	perc = round(float(count) / len(contig_list) * 100, 2)

	return '{} % of the contigs with length < {} bp'.format(perc, bp)
			
			
		
		
processed = 'Drad_unigene.fasta'
original = 'Trinity.fasta'

proc_contig_tuple, proc_contig_dict = ContigLen(processed)
orig_contig_tuple, orig_contig_dict = ContigLen(original)



print(proc_contig_tuple)
print(FreqLen(proc_contig_tuple, 300))
print(orig_contig_tuple)
print(FreqLen(orig_contig_tuple, 300))


