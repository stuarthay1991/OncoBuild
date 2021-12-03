#Data clean

import preprocessing as prep
prep.moveTo(prep.LAMLdatadir)
infile = open(prep.objects[1], "r")
colfile = open((prep.objects[1]+".columns"), "w")
sampleinds = prep.findSampleIndsWriteColFile(infile, colfile)
stats = prep.loopThroughFile(infile, "stat", sampleinds)
stat1 = stats["data1"]
filemaxcols = max(stat1)
filemincols = min(stat1)
outfilename = prep.objects[1] + ".stat"
outfile = open(outfilename, "w")
outfile.write(str(filemaxcols))
outfile.write("\n")
outfile.write(str(filemincols))
outfile.close()