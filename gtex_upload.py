rootpath = "/data/salomonis2/NCI-R01/ONCObrowser/Gtex/pgr.txt"

basket = []
rootfile = open(rootpath, "r")
colfile = open("/data/salomonis2/NCI-R01/ONCObrowser/Gtex/gtex_cols.txt", "w")
matrixfile = open("/data/salomonis2/NCI-R01/ONCObrowser/Gtex/gtex_matrix.txt.csv", "w")

cols = next(rootfile)
cols = cols.rstrip()
cols = cols.replace(" ","_")
cols = cols.replace("-","")
cols = cols.replace("__","_")
cols = cols.split("\t")
cols.insert(0, "UID")

print(len(cols))
print(cols)

cols = "\t".join(cols)
colfile.write(cols)

all_lens = []

mc = 0

try:
	while True:
		line = next(rootfile)
		p = line.split("\t")
		all_lens.append(len(p))
		p = p[0:52]
		p = "#".join(p)
		matrixfile.write(p)
		matrixfile.write("\n")
	print("Finished1")
except:
	print("Finished2")

print(list(set(all_lens)))
colfile.close()
rootfile.close()
matrixfile.close()