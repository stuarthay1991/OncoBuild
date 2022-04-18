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
    print(("COL NUM = " + str(len(line))))
    lineToCsv = ",".join(newline)
    outfile.write(lineToCsv)
    outfile.close()
    for index in range(len(line)):
        if(line[index][0:4] == "TCGA" or line[index][-4:] == ".bed"):
            ret_arr.append(index)
    return ret_arr, repeatanswer

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
                corrected_line = fillInRowSplicingValues(line, sampleinds, filemaxcol, filemincol, repeatindex)
                if(corrected_line != "NAN"):
                    outfile.write(corrected_line)
                    outfile.write("\n")
                else:
                    #print(corrected_line)
                    continue
        return ret_val
    except:
        var = traceback.format_exc()
        #e = sys.exc_info()
        #print("BREAK", var)
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
    line = line.rstrip()
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
        #if(i >= total_vals):
            #break
        #if(line[i] != ""):
            #givenvals.append(float(line[i]))
    #try:
    #working_mean = numpy.median(givenvals)
    #except:
        #print(line, repeatindex, inds, total_vals, punkey)
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
                okl = float(line[i]) #- working_mean
                okl = round(okl, 2)
                okl = str(okl)
                correct_line.append(okl)
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


def metaSet(infile, outfile, colfile, tdict, delimiter="\t"):
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
            cur_string_examined = line[i];
            if(cur_string_examined.find("/") != -1):
                cur_string_examined = cur_string_examined.replace("/", "_")
            newcolline.append(cur_string_examined)

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
            extracted_set.append(line[uid_col_num])
            ecount += 1
            count += 1
    except:
        return extracted_set