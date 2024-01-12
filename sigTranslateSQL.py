import psycopg2
import traceback
import os

querybox = []
inDirPath = "/data/salomonis2/NCI-R01/ONCObrowser/Completed"
inDirContents = os.listdir(inDirPath)
uploadLabels = ["cancer", "clusters", "psi_event_signatures", "simple_name"]
uploadTable = [[], [], [], []]
for cancerDir in inDirContents:
	if(cancerDir != ".DS_Store"):
		inFile = "/data/salomonis2/NCI-R01/ONCObrowser/Completed/" + cancerDir + "/Oncosplice-translation.txt"
		cancerName = cancerDir.replace("-", "_")
		print(cancerName)
		openedInFile = open(inFile, "r")
		lineCount = 0
		for line in openedInFile:
			if lineCount == 0:
				lineCount = lineCount + 1
				continue
			line = line.rstrip()
			inputData = line.split("\t")
			uploadTable[0].append(cancerName)
			uploadTable[1].append(inputData[0])
			uploadTable[2].append(inputData[1])
			uploadTable[3].append(inputData[2])

dumpFile = open("/data/salomonis2/NCI-R01/ONCObrowser/dumpTranslation.csv", "w")
for i in range(len(uploadTable[0])):
	dumpString = uploadTable[0][i] + "#" + uploadTable[1][i] + "#" + uploadTable[2][i] + "#" + uploadTable[3][i] + "\n"
	dumpFile.write(dumpString)

dumpFile.close()

queryobj1 = "CREATE TABLE SIGTRANSLATE" + " (\n"
for i in range(len(uploadLabels)):
	oldstr = uploadLabels[i]
	newstr = oldstr.replace("-", "_")
	newstr = newstr.replace(".", "_")
	newstr = newstr.replace(" ", "_")
	newstr = newstr.replace("(", "_")
	newstr = newstr.replace(")", "_")
	if(i != (len(uploadLabels) - 1)):
		query_set = newstr + " " + "TEXT ,\n"
	else:
		query_set = newstr + " " + "TEXT \n"
	queryobj1 = queryobj1 + query_set
queryobj1 = queryobj1 + ");\n"


queryobj2 = "COPY SIGTRANSLATE" + "\n"
queryobj2 = queryobj2 + "FROM '/data/salomonis2/NCI-R01/ONCObrowser/dumpTranslation.csv'" + "\n"
queryobj2 = queryobj2 + "DELIMITER '#';"

#queryobj3 = "CREATE UNIQUE INDEX " + "GTEXuid_btree_index ON " + "GTEX" + " USING btree(UID);"
#querybox.append(queryobj0)
querybox.append(queryobj1)
querybox.append(queryobj2)
#querybox.append(queryobj3)

try:
	conn = psycopg2.connect("dbname='oncocasen' user='haym4b' host='127.0.0.1' password=''")
	print("Connection win")
	#print(SQL)
	cur = conn.cursor()
	for i in querybox:
		try:
			print("Currently executing...", i)
			cur.execute(i)
			print("Execution complete")
		except:
			var = traceback.format_exc()
			print(var)
			print("connection rollback.")
			conn.rollback()
	conn.commit()
	cur.close()
	conn.close()
	print("SQL win")
except:
	print("Something failed")
	var = traceback.format_exc()
	print(var)

