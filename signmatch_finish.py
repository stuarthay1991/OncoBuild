import preprocessingV2 as prep
import numpy
def setupSignature(cancer):
	prep.moveTo(cancer.rootpath)
	target_dir = "DE_splicing_events/Events-dPSI_0.1_adjp"
	try:
		file_list = prep.listdir("DE_splicing_events/Events-dPSI_0.1_adjp")
	except:
		target_dir = "DE_splicing-events/Events-dPSI_0.1_adjp"
		file_list = prep.listdir(target_dir)
	uidpile = []
	uiddict = {}
	uidind = {}
	filedict = {}
	files = []
	#class Oncosignature:
	#    def __init__(self):
	#        self.type = []
	#        self.set = []
	#    def mapTypes(self, trick):
	#        self.tricks.append(trick)


	for i in file_list:
		if(i != ".DS_Store" and i != "event_summary.txt"):
			files.append(i)
			filepath = target_dir + "/" + i
			openfile = open(filepath, "r")
			uidcur = prep.extractUID(openfile)
			#print(uidcur)
			uiddict[i] = uidcur
			openfile.close()
			uidpile.extend(uidcur)
	uidset = set(uidpile)

	columns = ["UID"]
	files_e = "\t".join(files)
	files_e = files_e.replace(".txt", "")
	files_e = files_e.split("\t")
	columns.extend(files_e)
	columns = "#".join(columns) + "\n"
	columns = columns.replace("psi", "");
	columns = columns.replace("+", "positive_")
	columns = columns.replace("", "_")

	uidset = list(uidset)

	for i in range(len(uidset)):
		uidind[uidset[i]] = i

	for i in range(len(files)):
		filedict[files[i]] = i

	rows = []
	arrayset = numpy.zeros(((len(uidset)), (len(files))))

	for k in files:
		for i in uiddict[k]:	
			arrayset[uidind[i], filedict[k]] = 1

	#print(arrayset)

	oncosig = open("ToPostgres/oncosig.txt", "w")
	oncosig.write(columns)
	for i in range(len(arrayset)):
	  p = list(arrayset[i])
	  t = []
	  for u in p:
	  	u = str(int(u))
	  	t.append(u)
	  t = "#".join(t)
	  t = uidset[i] + "#" + t + "\n"
	  oncosig.write(t)
	oncosig.close()
#infile1 = open(prep.objects[1], "r")
#infile2 = open(prep.objects[2], "r")

#matched = prep.extractUID(infile1)

#print(matched)