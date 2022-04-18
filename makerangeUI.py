#Make Range UI

import preprocessingV3 as prep
import os
import numpy

class SampleAttribute:
	def __init__(self, filepath, fname):
		self.filepath = filepath
		self.fname = fname
		self.type = "NAN"
		self.uniquevalues = "NAN"
		self.values = "NAN"
		self.range = "NAN"
		self.min = "NAN"
		self.max = "NAN"
		self.boundary1 = "NAN"
		self.boundary2 = "NAN"
	
	def setUniqueVals(self, number):
		self.uniquevalues = number
	
	def setType(self, filtertype):
		self.type = filtertype

	def setValues(self, values):
		self.values = values

	def runCalculations(self):
		self.max = max(self.values)
		self.min = min(self.values)
		self.range = self.max - self.min
		self.boundary1 = self.min + int(self.range * 0.33)
		self.boundary2 = self.max - int(self.range * 0.33)

def annotate(filepath, fname):
	def iterateline(input):
		counts = 0
		filtertype = "int"
		inputs = []
		for i in input:
			try:
				modified = int(i)
				inputs.append(modified)
			except:
				if(i == "NA"):
					inputs.append(0)
				elif(i == "-"):
					inputs.append(0)
				elif(i == "nan"):
					inputs.append(0)
				elif(i == "--"):
					inputs.append(0)
				elif(i == "---"):
					inputs.append(0)
				elif(i == " "):
					inputs.append(0)
				elif(i == ""):
					inputs.append(0)
				else:
					filtertype = "nonint"
					inputs.append(i)
		return inputs, filtertype
	cur_filter = SampleAttribute(filepath, fname)
	openfile = open(cur_filter.filepath, "r")
	line = next(openfile)
	line = line.rstrip()
	line = line.split("#")
	inputs, inputtype = iterateline(line)
	cur_filter.setUniqueVals(len(inputs))
	cur_filter.setType(inputtype)
	cur_filter.setValues(inputs)
	return cur_filter

def make(cancer):
	SampleList = []
	try:
		os.mkdir("Range")
	except:
		print("Made range directory.")
	prep.moveTo(cancer.rootpath)
	dirlist = os.listdir("Columns")
	for i in dirlist:
		#print(i)
		retsample = annotate(("Columns/" + i), i)
		SampleList.append(retsample)

	for i in SampleList:
		if(i.uniquevalues > 20 and i.type == "int"):
			i.runCalculations()
			if(i.min >= 0):
				newfile = open(("Range/" + i.fname), "w")
				newfile.write(str(i.min))
				newfile.write("-")
				newfile.write(str(i.boundary1))
				newfile.write("#")
				newfile.write(str(i.boundary1))
				newfile.write("-")
				newfile.write(str(i.boundary2))
				newfile.write("#")
				newfile.write(str(i.boundary2))
				newfile.write("-")
				newfile.write(str(i.max))
				newfile.close()
