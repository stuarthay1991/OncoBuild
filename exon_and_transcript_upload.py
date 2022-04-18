import psycopg2
import traceback
import os

os.chdir("/data/salomonis2/NCI-R01/ONCObrowser/GeneModel")

exontxt = open("Hs_Ensembl_exon.txt", "r")
transtxt = open("Hs_Ensembl_transcript-annotations.txt", "r")
junctxt = open("Hs_Ensembl_junction.txt", "r")

exoncols = open("exoncols.txt", "w")
transcols = open("transcols.txt", "w")
junccols = open("junccols.txt", "w")

exonfin = open("exonfin.csv", "w")
transfin = open("transfin.csv", "w")
juncfin = open("juncfin.csv", "w")

exontocols = next(exontxt)
transtocols = next(transtxt)
junctocols = next(junctxt)

exontocols.rstrip()
transtocols.rstrip()
junctocols.rstrip()

print(len(transtocols.split("\t")))

exoncols.write(exontocols)
transcols.write(transtocols)
junccols.write(junctocols)

ex_basket = []
count10 = 0
count9 = 0
count8 = 0
count7 = 0

while(True):
	try:
		line = next(exontxt)
		line = line.rstrip()
		line = line.split("\t")
		ex_basket.append(len(line))
		cur_add = []
		for item_index in range(len(line)):
			if(line[item_index] == ""):
				cur_add.append("NA")
			else:
				cur_add.append(line[item_index])
		while(len(cur_add) < 10):
			cur_add.append("NA")
		newline = "#".join(cur_add)
		newline = newline + "\n"
		exonfin.write(newline)
	except:
		print("Stop iteration")
		break

print(count7)
print(count8)
print(count9)
print(count10)
print(list(set(ex_basket)))

tr_basket = []

while(True):
	try:
		line = next(transtxt)
		line = line.rstrip()
		line = line.split("\t")
		tr_basket.append(len(line))
		line = "#".join(line)
		line = line + "\n"
		transfin.write(line)
	except:
		print("Stop iteration")
		break

print(list(set(tr_basket)))

junc_basket = []

while(True):
	try:
		line = next(junctxt)
		line = line.rstrip()
		line = line.split("\t")
		junc_basket.append(len(line))
		cur_add = []
		for item_index in range(len(line)):
			if(line[item_index] == ""):
				cur_add.append("NA")
			else:
				cur_add.append(line[item_index])
		while(len(cur_add) < 10):
			cur_add.append("NA")
		newline = "#".join(cur_add)
		newline = newline + "\n"
		juncfin.write(newline)
	except:
		print("Stop iteration")
		break

print(list(set(tr_basket)))
print(list(set(junc_basket)))

exontxt.close()
transtxt.close()

exoncols.close()
transcols.close()

exonfin.close()
transfin.close()
