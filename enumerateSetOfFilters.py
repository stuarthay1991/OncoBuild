#Data clean

import preprocessingV2 as prep
import os

def make(cancer):
	prep.moveTo(cancer.rootpath)

	try:
		os.mkdir("Columns")
	except:
		print("Made columns directory.")
	infile = open(("ToPostgres/metadata.txt.pgr.csv"), "r")
	colfile = open(("ToPostgres/metadata.txt.columns"), "r")

	rawcol = next(colfile)
	rawcol = rawcol.rstrip()
	rawcol = rawcol.split(",")

	coldict = {}

	try:
		while(True):
			line = next(infile)
			line = line.rstrip()
			line = line.split("#")
			for i in range(1, len(line)):
				try:
					coldict[rawcol[i]].append(line[i])
				except:
					coldict[rawcol[i]] = []
	except:
		print("Done")

	moldict = {}
	toldict = {}

	for i in coldict:
		moldict[i] = list(set(coldict[i]))

	for i in coldict:
		new_arr = []
		for k in moldict[i]:
			count = 0
			for j in coldict[i]:
				if(j == k):
					count = count + 1
			new_arr.append(k)
		i = i.replace("/", "_")
		toldict[i] = new_arr
	
	#print("toldict", toldict)
	for i in toldict:
		f = open(("Columns/"+i+".txt"), "w")
		tofile = "#".join(toldict[i]) + "\n"
		f.write(tofile)
		f.close()
