import preprocessingV3 as prep
import numpy

def mapAll(cancer):
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

        full_event_file_name = "ToPostgres/detailedSignature.csv"
        full_event_file = open(full_event_file_name, "w")

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
                        periodsplit = i.split(".")
                        if(len(periodsplit) == 3):
                                signaturename = periodsplit[1]
                        else:
                                signaturename = periodsplit[2]
                        signaturename = "psi_" + signaturename
                        signaturename = signaturename.replace(".", "_");
                        signaturename = signaturename.replace("-", "_");
                        signaturename = signaturename.replace("(", "_");
                        signaturename = signaturename.replace(")", "_");
                        signaturename = signaturename.lower()
                        filepath = target_dir + "/" + i
                        openfile = open(filepath, "r")
                        line = next(openfile)
                        line = line.rstrip()
                        line = line.split("\t")
                        possibleColumns = {"UID": -1,
                                           "Event-Direction": -1,
                                           "ClusterID": -1,
                                           "EventAnnotation": -1,
                                           "Coordinates": -1,
                                           "ProteinPredictions": -1,
                                           "dPSI": -1,
                                           "rawp": -1,
                                           "adjp": -1,
                                           "avg-Others": -1}
                        keysList = list(possibleColumns.keys())
                        for k in range(len(line)):
                                for j in keysList:
                                        if(j.lower() == line[k].lower()):
                                              possibleColumns[j] = k
                                              break
                        try:
                                while(True):
                                        line = next(openfile)
                                        line = line.rstrip()
                                        line = line.split("\t")
                                        line_make = [signaturename]
                                        for m in keysList:
                                                if(possibleColumns[m] == -1):
                                                        line_make.append("NA")
                                                else:
                                                        line_make.append(line[possibleColumns[m]])
                                        line_write = "#".join(line_make) + "\n"
                                        line_write = line_write.replace("'", "");
                                        full_event_file.write(line_write)
                        except:
                                openfile.close()
	
        full_event_file.close()
