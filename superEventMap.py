import preprocessingV3 as prep
import numpy

def setupFile():
    super_event_file = open("supereventtable.csv", "w")
    super_event_file.close()


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

    super_event_file_name = "../supereventtable.csv"
    super_event_file = open(super_event_file_name, "a")

    filedict = {}
    files = []

    for i in file_list:
        if(i != ".DS_Store" and i != "event_summary.txt"):
                files.append(i)
                signaturename = i[0:-4]
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
                possibleColumns = {"UID": -1,"Event-Direction": -1,"ClusterID": -1,"EventAnnotation": -1}
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
                        line_make = [cancer.name.replace("-", "_"), signaturename]
                        for m in keysList:
                            if(possibleColumns[m] == -1):
                                line_make.append("NA")
                            else:
                                if(m == "UID"):
                                    firstJunc = line[possibleColumns[m]].split("|")[0]
                                    line_make.append(firstJunc)
                                line_make.append(line[possibleColumns[m]])
                        line_write = "#".join(line_make) + "\n"
                        line_write = line_write.replace("'", "");
                        super_event_file.write(line_write)
                except:
                    openfile.close()
    super_event_file.close()
