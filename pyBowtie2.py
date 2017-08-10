class runAlignment(object):
	"""pyBowtie2 class that runs bowtie2 to create sam files with Read group for GAKT
	depth of coverage analysis
	"""

	def __init__(self, fq):
		self.fq = fq

		
	def __str__(self):
		return self.fq
		
		
	def getRG(self):
		"""
		this will return a dictionary for run_bowtie2 function
		"""
		
		assert str(self.fq)[-2:] == 'fq', "Must be a fq file"
		
		if str(self.fq)[7:9] == '24':		
		
			path = '/home/swaggyp1985/Desktop/Drad/trimReads/G24/' + self.fq
		
			
		elif str(self.fq)[7:9] == '34':
			
			path = '/home/swaggyp1985/Desktop/Drad/trimReads/G34/' + self.fq
			
			
			
		fh = open(path, 'r')
			
		
		
		rg = {}
		
		for line in fh:
			if line.startswith('@HISEQ2'):
				instr = line.split()[0].split(':')[0].split('@')[1]
				run_num = line.split()[0].split(':')[1]
				flowcell = line.split()[0].split(':')[2]
				lane = line.split()[0].split(':')[3]
				read = line.split()[1].split(':')[0]
				sample_num = line.split()[1].split(':')[3]


				rg['ID'] = run_num + '.' + flowcell + '.' + lane
				rg['PL'] = 'illumina' + '.' + instr
				rg['LB'] = str(self.fq)[0:10]
				rg['SM'] = str(self.fq)[0:10]
				rg['PATH'] = path
				
				break

		return rg
		
	def createDir(self):
		"""create a directory for index in the current directory"""
		
		folders = Popen(['ls'], stdout = PIPE, stderr = PIPE).communicate()
		
		if not 'index' in folders[0].split():
			Popen(['mkdir', 'index'], stdout = PIPE, stderr = PIPE)
			
		if not 'G24' in folders[0].split():
			Popen(['mkdir', 'G24'], stdout = PIPE, stderr = PIPE)
			
		if not 'G34' in folders[0].split():
			Popen(['mkdir', 'G34'], stdout = PIPE, stderr = PIPE)
		
		if str(self.fq)[7:9] == '24':
			Popen(['mkdir', self.fq], stdout = PIPE, stderr = PIPE, cwd = 'G24')
		elif str(self.fq)[7:9] == '34':
			Popen(['mdkir', self.fq], stdout = PIPE, stderr = PIPE, cwd = 'G34')

				
	def createIndex(self, path):
		"""create index of the fasta file
		path1: a string. Path to the assembly fasta
		"""
		
		comnd = "bowtie2-build " + '../' + path + " newTrinity.fasta"
		
		print('Building index ... Command executed: {}\n'.format(comnd))
		
		comnd_input = shlex.split(comnd)		
		# newTrinity is two levels from index
		Popen(comnd_input, stdout = PIPE, stderr = PIPE, 
					cwd = 'index')
					
					
					
		
	def run_bowtie2(self, arg_dict):
		"""
		arg_dict: a dictionary contains
	
		ID, PL, LB, SM
		"""
		print('Running bowtie2 on {0[LB]} ... '.format(arg_dict))
		
		
		
		
		if str(self.fq)[7:9] == '24':
			
			
			# need to make sure the path is correct
			cli1 = "\
			bowtie2 \
			-p 4 \
			-q \
			-x '../../index/newTrinity.fasta' \
			-U {0[PATH]} \
			--rg-id {0[ID]} \
			--rg ID:{0[ID]} \
			--rg PL:{0[PL]} \
			--rg LB:{0[LB]} \
			--rg SM:{0[SM]} \
			-S {0[LB]}.sam".format(arg_dict)
	
			cli1 = shlex.split(cli1)
			c1_out = Popen(cli1, stdout = PIPE, stderr = PIPE, cwd = 'G24/'+ str(self.fq))
			
		elif str(self.fq)[7:9] == '34':
			
			cli1 = "\
			bowtie2 \
			-p 4 \
			-q \
			-x '../../index/newTrinity.fasta' \
			-U {0[PATH]} \
			--rg-id {0[ID]} \
			--rg ID:{0[ID]} \
			--rg PL:{0[PL]} \
			--rg LB:{0[LB]} \
			--rg SM:{0[SM]} \
			-S {0[LB]}.sam".format(arg_dict)
	
			cli1 = shlex.split(cli1)
			c1_out = Popen(cli1, stdout = PIPE, stderr = PIPE, cwd = 'G34/'+ str(self.fq))
			

		return c1_out		

	def sam2bam(self):
		"""
		return bam file in the working directory
		"""
		
		if str(self.fq)[7:9] == '24':
			# create bam
			comnd = "samtools view -bS " + str(self.fq)[0:10] + ".sam > " + str(self.fq)[0:10]  + ".bam"
		
			print("Converting sam to bam ...\n") 
			print('executed command: {} \n'.format(comnd))

			p1 = Popen(comnd, stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True, cwd = 'G24/' + str(self.fq))
					
		elif str(self.fq)[7:9] == '34':
			# create bam
			comnd = "samtools view -bS " + str(self.fq)[0:10]  + ".sam > " + str(self.fq)[0:10]  + ".bam"
		
			print("Converting sam to bam ... \n")
			print("executed command: {}\n".format(comnd))
#			comnd_input  = shlex.split(comnd)

			p1 = Popen(comnd, stdin = PIPE, stdout = PIPE, stderr = PIPE, cwd = 'G34/' + str(self.fq))
			
			
			
		return p1
		
		
		
	def sortBam(self):
		""" sort the bam file in the directory"""
			
		if str(self.fq)[7:9] == '24':
			# sort bam		
			comnd2 = "samtools sort " + str(self.fq)[0:10]  + ".bam -o " + str(self.fq)[0:10]  + ".sorted.bam"	
			print('Sorting bam ... \n')
			print('executed command: {}\n'.format(comnd2))
		
			comnd_input2  = shlex.split(comnd2)

			p2 = Popen(comnd_input2, stdin = PIPE, stdout = PIPE, stderr = PIPE, cwd = 'G24/' + str(self.fq))
			
		elif str(self.fq)[7:9] == '34':
			# sort bam
			comnd2 = "samtools sort " + str(self.fq)[0:10]  + ".bam -o " + str(self.fq)[0:10]  + ".sorted.bam"	
			print('Sorting bam ...\n')
			print('executed command: {}\n'.format(comnd2))
		
			comnd_input2  = shlex.split(comnd2)

			p2 = Popen(comnd_input2, stdin = PIPE, stdout = PIPE, stderr = PIPE, cwd = 'G34/' + str(self.fq))
			
			
		return p2


	def indexBam(self):
		"""index the sorted bam file in the directory"""
			
		if str(self.fq)[7:9] == '24':
			# index bam
			comnd3 = "samtools index " + str(self.fq)[0:10]  + ".sorted.bam"	
			print('Indexing bam ... \n')
			print('executed command: {}\n'.format(comnd3))
		
			comnd_input3  = shlex.split(comnd3)

			p3 = Popen(comnd_input3, stdin = PIPE, stdout = PIPE, stderr = PIPE, cwd = 'G24/' + str(self.fq))

					
		elif str(self.fq)[7:9] == '34':
			
			# index bam
			comnd3 = "samtools index " + str(self.fq)[0:10]  + ".sorted.bam"	
			print('Indexing bam ... \n')
			print('executed command: {}\n'.format(comnd3))
		
			comnd_input3  = shlex.split(comnd3)

			p3 = Popen(comnd_input3, stdin = PIPE, stdout = PIPE, stderr = PIPE, cwd = 'G34/' + str(self.fq))
			
		return p3
			
