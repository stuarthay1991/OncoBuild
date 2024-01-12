import preprocessingV3 as prep
import numpy

def mapAll(cancer):
        prep.moveTo(cancer.rootpath)
        target_dir = "DE_genes/2_Fold/DEGs-LogFold_1.0_adjp"
        file_list = prep.listdir(target_dir)

        uidpile = []
        uiddict = {}
        uidind = {}

        full_event_file_name = "ToPostgres/detailedDE.csv"
        full_event_file = open(full_event_file_name, "w")

        filedict = {}
        files = []

        for i in file_list:
                if(i != ".DS_Store" and i != "gene_summary.txt"):
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
                        print(line)
                        gene_full = []
                        try:
                                while(True):
                                        line = next(openfile)
                                        line = line.rstrip()
                                        line = line.split("\t")
                                        if(line[5] == "" or line[5] == " "):
                                            line[5] = "NA"
                                        line.insert(0, signaturename)
                                        line_write = "#".join(line) + "\n"
                                        full_event_file.write(line_write)
                        except:
                                #print("file closed")
                                openfile.close()
        full_event_file.close()
