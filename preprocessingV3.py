#Preprocessing

import sys, os, numpy, traceback

numpy.seterr(all='raise')

def moveTo(path):
    os.chdir(path)

def mkdir(name):
    os.mkdir(name)

def listdir(path):
    return os.listdir(path)

def nxtsplstrp(file, delimiter):
    line = next(file)
    line = line.rstrip()
    line = line.split(delimiter)
    #print(line)
    return line

def nxtsplstrpspc(file, delimiter):
    line = next(file)
    line = line.replace("'", "")
    line = line.replace("(", "_")
    line = line.replace(")", "_")
    line = line.rstrip()
    line = line.split(delimiter)
    #print(line)
    return line


def checkForRepeats(cols):
    colrepeat = 0
    count = 0
    repeatindex = []
    for i in range(len(cols)):
        for k in range(len(cols)):
            if(cols[i] == cols[k]):
                count = count + 1
                if(count > 1):
                    repeatindex.append(k)
        count = 0
    return repeatindex


def findSampleIndsWriteColFile(infile, outfile, delimiter="\t"):
    ret_arr = []
    line = nxtsplstrp(infile, delimiter)
    newline = []
    for i in line:
        i = i.replace(" ", "_")
        newline.append(i)
    repeatanswer = checkForRepeats(newline)
    newabsline = []
    absline = []
    for i in range(len(line)):
        found = False
        for k in repeatanswer:
            if(k == i):
                found = True
                break
        if(found == False):
            newabsline.append(newline[i])
            absline.append(line[i])
    newline = newabsline
    line = absline
    newline = makeCoordCols(newline);
    newline = makePanUidCol(newline);
    line = newline
    print(("COL NUM = " + str(len(line))))
    lineToCsv = ",".join(newline)
    outfile.write(lineToCsv)
    outfile.close()
    for index in range(len(line)):
        if(line[index][0:4] == "TCGA" or line[index][-4:] == ".bed"):
            ret_arr.append(index)
    return ret_arr, repeatanswer

def makeCoordCols(line):
    coorcolindex = 0;
    for i in range(len(line)):
        if(line[i] == "Coordinates"):
            coorcolindex = i
            break
    line[coorcolindex] = "chromosome"
    line.insert((coorcolindex+1), "coord1")
    line.insert((coorcolindex+2), "coord2")
    line.insert((coorcolindex+3), "coord3")
    line.insert((coorcolindex+4), "coord4")
    return line

def makePanUidCol(line):
    line.insert(9, "pancanceruid")
    return line

def splitCoords4(line, repeatindex):
    try:
        line = line.rstrip()
        line = line.split("\t")
        wholesplit = line[9].split("|")
        coord1 = wholesplit[0]
        coord2 = wholesplit[1]
        coord1_chrm_split = coord1.split(":")
        coord1_chrm = coord1_chrm_split[0]
        coord1_numbers = coord1_chrm_split[1]

        coord1_numbers_split = coord1_numbers.split("-")
        coord1_numbers_start = coord1_numbers_split[0]
        coord1_numbers_end = coord1_numbers_split[1]

        coord2_chrm_split = coord2.split(":")
        coord2_chrm = coord2_chrm_split[0]
        coord2_numbers = coord2_chrm_split[1]

        coord2_numbers_split = coord2_numbers.split("-")
        coord2_numbers_start = coord2_numbers_split[0]
        coord2_numbers_end = coord2_numbers_split[1]

        line[9] = coord1_chrm
        line.insert(10, coord1_numbers_start)
        line.insert(11, coord1_numbers_end)
        line.insert(12, coord2_numbers_start)
        line.insert(13, coord2_numbers_end)
        line = "\t".join(line)
    except:
        print("Coordsplit failed")
    return line

def addPanCancerUID(line):
    try:
        line = line.rstrip()
        line = line.split("\t")
        wholesplit = line[8].split("|")
        pancanceruid = wholesplit[0]
        line.insert(9, pancanceruid)
        line = "\t".join(line)
    except:
        print("PanCancerAdd failed")
        var = traceback.format_exc()
        print(var)
    return line

def loopThroughFile(infile, flag, sampleinds="", outfile="", filemaxcol=0, filemincol=0, repeatindex=[]):
    if(flag == "stat"):
        ret_val = {"data1": []}
    else:
        ret_val = {"data1": []}
    try:
        while(True):
            line = next(infile)
            if(flag == "stat"):
                ret_val["data1"].append(findRowSplicingStats(line, repeatindex))
            if(flag == "clean"):
                #print("LINE")
                corrected_line = splitCoords4(line, repeatindex)
                corrected_line = addPanCancerUID(corrected_line)
                corrected_line = fillInRowSplicingValues(corrected_line, sampleinds, filemaxcol, filemincol, repeatindex)
                if(corrected_line != "NAN"):
                    outfile.write(corrected_line)
                    outfile.write("\n")
                else:
                    #print(corrected_line)
<<<<<<< HEAD
                    #print("NAN is not a valid value, please reformat")
=======
>>>>>>> 6ce566add9a01b5439cb3503208c1232aea57bf6
                    continue
        return ret_val
    except:
        var = traceback.format_exc()
        #e = sys.exc_info()
        print("BREAK", var)
        infile.close()
        return ret_val

def printSpecificLine(infile, condition, prop):
    try:
        while(True):
            line = nxtsplstrp(infile, "\t")
            if(condition == "length"):
                if(len(line) == prop):
                    print(line)
                    return
    except:
        return

def findRowSplicingStats(line, repeatindex):
    line = line.rstrip()
    line = line.split("\t")
    return (len(line) - len(repeatindex))

def fillInRowSplicingValues(line, inds, filemaxcol, filemincol, repeatindex):
    line = line.split("\t")
    absline = []
    punkey = line
    #print("STOP1")
    for i in range(len(line)):
        found = False
        for k in repeatindex:
            if(k == i):
                found = True
                break
        if(found == False):
            absline.append(line[i])
    line = absline
    total_vals = len(line)
    givenvals = []
    #print("STOP2")
    #for i in inds:
    #    if(i >= total_vals):
    #        break
    #    if(line[i] != ""):
    #        givenvals.append(float(line[i]))
    #try:
    #    working_mean = numpy.median(givenvals)
    #except:
    #    return "NAN"
    #working_mean = round(working_mean, 2)
    correct_line = []
    #print("STOP3", inds, filemaxcol)
    for i in range(filemaxcol):
        if(i >= total_vals):
            correct_line.append("0")
        elif(line[i] == ""):
            if(i < inds[0]):
                correct_line.append("NA")
            else:
                correct_line.append("0")
        else:
            try:
                if(i >= inds[0]):
                    okl = float(line[i])# - working_mean
                    okl = round(okl, 2)
                    okl = str(okl)
                    correct_line.append(okl)
                else:
                    correct_line.append(line[i])
            except:
                correct_line.append(line[i])
    #print("STOP4")
    correct_line = "#".join(correct_line)
    if(len(correct_line.split("#")) != filemaxcol):
        print("Missing Columns: ", len(correct_line.split("#")))
        return "NAN"
    else:
        return correct_line    

def findFileLength(infile):
    starting_num = 0
    try:
        while(True):
            line = next(infile)
            starting_num += 1
    except:
        return starting_num
    
def translateMeta(infile, delimiter="\t"):
    translate_arr = {}
    next(infile)
    try:
        while(True):
            line = next(infile)
            line = line.rstrip()
            line = line.split(delimiter)
            translate_arr[line[1]] = line[0]
        infile.close()
    except:
        infile.close()
        return translate_arr


def metaSet(infile, outfile, colfile, tdict, cname, delimiter="\t"):
    ret_arr = []

    line = nxtsplstrpspc(infile, delimiter)
    repeat_index = checkForRepeats(line)
    print("META REPEAT", repeat_index)
    truelength = len(line)
    if(len(repeat_index) == 0):
        repeat_index = "NA"
    else:
        repeat_index = repeat_index[0]
    newcolline = []
    print(("COL NUM = " + str(len(line))))
    line[0] = "uid"
    for i in range(len(line)):
        if(i != repeat_index):
            newcolline.append(line[i])

    for i in range(len(line)):
        try:
            int(line[i][0])
            line[i] = "Y" + line[i]
        except: 
            continue
    lineToCsv = ",".join(newcolline)
    colfile.write(lineToCsv)
    colfile.close()
    try:
        while(True):
            line = next(infile)
            line = line.rstrip()
            line = line.split(delimiter)
            for i in range(truelength):
                if(i != repeat_index):
                    try:
                        if(i == 0):
                            if(cname == "AML-Leucegene"):
                                modif = line[i]
                                if(modif[-4:] == ".bed"):
                                    modif = modif[0:-4]
                                outfile.write(tdict[modif])
                            else:
                                outfile.write(tdict[line[i]])
                        elif(len(line[i]) == 0):
                            outfile.write("NA")
                        else:
                            outfile.write(line[i])
                        if(i != (truelength-1)):
                            outfile.write("#")
                    except:
                        outfile.write("NA")
                        if(i != (truelength-1)):
                            outfile.write("#")
            outfile.write("\n")
        outfile.close()
    except:
        outfile.close()
        return

def removeMiss(infile, colfile, outfile, delimiter="#"):
    col_match = next(colfile)
    col_match = col_match.rstrip()
    col_match = col_match.split(",")
    try:
        while(True):
            line = next(infile)
            e_line = line.rstrip()
            e_line = e_line.split(delimiter)
            sample = e_line[0]
            for i in col_match:
                newcol = i[0:len(sample)]
                if(newcol == sample):
                    newl = "#".join(e_line[1:])
                    newl = i + "#" + newl + "\n"
                    outfile.write(newl)
                    break
    except:
        return

def extractUID(file):
    #print(file)
    count = 0
    cols = nxtsplstrp(file, "\t")
    uid_col_num = "NONE"
    extracted_set = []
    ecount = 0
    for i in range(len(cols)):
        if(cols[i] == "UID"):
            uid_col_num = i
            break
    if(uid_col_num == "NONE"):
        return "NONE"
    try:
        while(True):
            if(ecount > 200):
                return extracted_set
            line = nxtsplstrp(file, "\t")
            panuid = line[uid_col_num]
            panuid = panuid.split("|")
            panuid = panuid[0]
            extracted_set.append(panuid)
            ecount += 1
            count += 1
    except:
<<<<<<< HEAD
        return extracted_set
=======
        return extracted_set
>>>>>>> 6ce566add9a01b5439cb3503208c1232aea57bf6
