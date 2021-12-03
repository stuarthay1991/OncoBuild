import sys, os
import preprocessingV2 as P
import clean as C
#import upload as U
import metaset
import metaquery
import splicequery
import signmatch_finish
import signmatch_pgr
import enumerateSetOfFilters
import makerangeUI
#import psycopg2

print(os.getcwd())

objects = sys.argv
rootdir = "/data/salomonis2/NCI-R01/ONCObrowser"
datadir = rootdir

newdir = datadir + "/Completed"
olddir = datadir + "/old"

dattype = objects[1]
if(dattype == "new"):
	targetdir = newdir
	cancerlisting = os.listdir(newdir)
else:
	targetdir = datadir + "/" + dattype
	cancerlisting = os.listdir(targetdir)

CANCERS = []

class Cancer:
    def __init__(self, name, rootpath):
    	self.name = name
    	self.rootpath = rootpath
    	self.eventspath = ""
    	self.samplefilterpath = ""
    	self.signaturepath = ""
    	self.maxcols = ""
    	self.mincols = ""
    	self.sampleindices = ""
    	self.repeatindex = "NAN"

    def findEvents(self):
    	pre_eventpath = self.rootpath + "/PSI_File"
    	self.eventspath = pre_eventpath + "/Hs_RNASeq_top_alt_junctions-PSI_EventAnnotation.txt"

    def findMetadata(self):
    	self.metafile = "Clinical_metadata_fields/metadata.txt"

    def makeMeta(self):
    	metaset.make(self)
    	metaquery.make(self)

    def initStats(self):
    	C.makeStats(self)

    def cleanEvents(self):
    	C.makeClean(self)

    def makeSpliceSQL(self):
    	splicequery.makequery(self)

    def setupSig(self):
    	signmatch_finish.setupSignature(self)
    	signmatch_pgr.sigQuery(self)

    def enumFilters(self):
    	enumerateSetOfFilters.make(self)

    def makeRangeUI(self):
    	makerangeUI.make(self)

for i in cancerlisting:
	if(i != ".DS_Store"):
		cancerobj = Cancer(i, (targetdir + "/" + i))
		CANCERS.append(cancerobj)

for i in CANCERS:
	i.findEvents()
	print(i.eventspath)
	i.initStats()
	i.findMetadata()
	i.makeMeta()
	i.cleanEvents()
	i.makeSpliceSQL()
	i.setupSig()
	i.enumFilters()
	i.makeRangeUI()

#CANCERS[0].findMetadata()
#CANCERS[0].makeMeta()

#C.initClean(cancerlisting[0])
#metaset.make(cancerlisting[0])
#splicequery.makequery(cancerlisting[0])
#U.sync("splicequery.sql")
#metaquery.makequery(cancerlisting[0])
#U.sync("metaquery.sql")
