import sys, os
import preprocessingV3 as P
import clean as C
#import upload as U
import metaset
import metaquery
import splicequery
import signmatch_finish
import signmatch_pgr
import enumerateSetOfFilters
import makerangeUI
import makeComparison
#import psycopg2

print(os.getcwd())

objects = sys.argv
#rootdir = "/data/altanalyzeweb/AltAnalyze/ICGS/Oncosplice/testing/dbbuild"
rootdir = "/data/salomonis2/NCI-R01/ONCObrowser"
datadir = rootdir

newdir = datadir + "/Completed"
olddir = datadir + "/old"

dattype = objects[1]
if(dattype == "new"):
        targetdir = newdir
        cancerlisting = os.listdir(newdir)
elif(dattype == "metalist"):
        targetdir = newdir
        cancerlisting = os.listdir(newdir)
        print("Comparing... ")
else:
        targetdir = datadir + "/" + dattype
        cancerlisting = os.listdir(targetdir)

CANCERS = []

class Cancer:
        def __init__(self, name, rootpath):
                self.name = name
                self.rootpath = rootpath
                self.eventspath = ""
                self.logpath = ""
                self.logfile = ""
                self.samplefilterpath = ""
                self.signaturepath = ""
                self.metafile = ""
                self.metapath = ""
                self.maxcols = ""
                self.mincols = ""
                self.sampleindices = ""
                self.repeatindex = "NAN"

        def setupLog(self):
                self.logpath = self.rootpath = "/report.txt";
                self.logfile = open(self.logpath, "w");
                return "Setup finished"

        def findEvents(self):
                pre_eventpath = self.rootpath + "/PSI_File"
                event_dir_contents = os.listdir(pre_eventpath)
                self.eventspath = "none";
                for i in event_dir_contents:
                        if(i[-3:] == "txt"):
                                self.eventspath = pre_eventpath + "/" + i
                                break
                if(self.eventspath == "none"):
                        raise ValueError("Input from the events folder does not exist.")
    	#self.eventspath = pre_eventpath + "/Hs_RNASeq_top_alt_junctions-PSI_EventAnnotation.txt"

        def findMetadata(self):
                self.metafile = "Clinical_metadata_fields/metadata.txt"
                self.metapath = self.rootpath + "/" + self.metafile

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

        def verifyEventToMetaMap(self):
                print("----------------")
                print(self.name)
                makeComparison.makeComparison(self)
                print("----------------")


for i in cancerlisting:
        if(i != ".DS_Store"):
                cancerobj = Cancer(i, (targetdir + "/" + i))
                CANCERS.append(cancerobj)

if(dattype == "new"):
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

if(dattype == "metalist"):
        print("Looking at columns in events and row keys in clinical metadata.")
        for i in CANCERS:
                i.findEvents()
                i.findMetadata()
                i.verifyEventToMetaMap()
#CANCERS[0].findMetadata()
#CANCERS[0].makeMeta()

#C.initClean(cancerlisting[0])
#metaset.make(cancerlisting[0])
#splicequery.makequery(cancerlisting[0])
#U.sync("splicequery.sql")
#metaquery.makequery(cancerlisting[0])
#U.sync("metaquery.sql")
