import preprocessingV3 as prep
import numpy

prep.moveTo(prep.LAMLdatadir)
target_dir = "OncoSplice_Signature"
file_list = prep.listdir("OncoSplice_Signature")
filetocompare = prep.objects[1]
f_cols = filetocompare + ".columns"
f_vals = filetocompare + ".pgr.csv"
uidpile = []
uiddict = {}
uidind = {}
filedict = {}
files = []
for i in file_list:
	if(i != ".DS_Store"):
		files.append(i)
		filepath = target_dir + "/" + i
		openfile = open(filepath, "r")
		uidcur = prep.extractUID(openfile)
		uiddict[i] = uidcur
		openfile.close()
		uidpile.extend(uidcur)

uidset = set(uidpile)
val_uids = []

colfile = open(f_cols, "r")
cols = next(colfile)
cols = cols.rstrip()
cols = cols.split(",")
UID_ind = 0
for i in range(len(cols)):
	if(cols[i] == "UID"):
		UID_ind = i
		break
colfile.close()

f_val_file = open(f_vals, "r")
try:
	while(True):
		line = next(f_val_file)
		line = line.rstrip()
		line = line.split("#")
		val_uids.append(line[UID_ind])
except:
	print("Google eye")
f_val_file.close()

#print(len(list(uidset)))
#print(len(val_uids))

burger = set(val_uids)

cheese = uidset.intersection(burger)

#print(len(list(burger)))