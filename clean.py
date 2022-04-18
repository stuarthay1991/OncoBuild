import preprocessingV3 as prep

def makeStats(cancer):
	prep.moveTo(cancer.rootpath)
	try:
		prep.mkdir("ToPostgres")
	except:
		print("Writing to directory 'ToPostgres'")
		infile = open(cancer.eventspath, "r")
		colfile = open(("ToPostgres/events.columns"), "w")
		cancer.sampleindices, repeatindex = prep.findSampleIndsWriteColFile(infile, colfile)
		cancer.repeatindex = repeatindex
		#print("REPEAT", repeatindex)
		stats = prep.loopThroughFile(infile, "stat", cancer.sampleindices, "", 0, 0, cancer.repeatindex)
		stat1 = stats["data1"]
		cancer.filemaxcols = max(stat1) + 5
		#print(cancer.filemaxcols, "MAXNUM")
		cancer.filemincols = min(stat1) + 5
		outfilename = "ToPostgres/events.stat"
		outfile = open(outfilename, "w")
		outfile.write(str(cancer.filemaxcols))
		outfile.write("\n")
		outfile.write(str(cancer.filemincols))
		outfile.close()
		#filestat = open(("events.stat"), "r")
		#filemaxcol = int(next(filestat))
		#print("MAX", filemaxcol)
		#filemincol = int(next(filestat))
		infile.close()
		outfile.close()

def makeClean(cancer):
	infile = open(cancer.eventspath, "r")
	outfile = open(("ToPostgres/events.pgr.csv"), "w")
	infile.seek(0, 0)
	next(infile)
	cleaned = prep.loopThroughFile(infile, "clean", cancer.sampleindices, outfile, cancer.filemaxcols, cancer.filemincols, cancer.repeatindex)
	outfile.close()
	infile.close()