#makedummymetaquery
import preprocessingV3 as prep

def make(cancer):
	prep.moveTo(cancer.rootpath)
	tfile = open("Sample-translation.txt", "r")
	translatedict = prep.translateMeta(tfile, delimiter="\t")
	infile = open(cancer.metafile, "r")
	colfile = open(("ToPostgres/" + "metadata.txt.columns"), "w")
	outfile = open(("ToPostgres/" + "metadata.txt.pgr.csv"), "w")
	prep.metaSet(infile, outfile, colfile, translatedict, cancer.name)