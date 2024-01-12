import psycopg2
import traceback
import os

os.chdir("/data/salomonis2/NCI-R01/ONCObrowser/GeneModel")

infilepath = "exoncols.txt"
infile = open(infilepath, "r")
infile_cols = next(infile)
infile_cols = infile_cols.rstrip()
infile_cols = infile_cols.split("\t")
infile.close()
querybox = []
print(len(infile_cols))

queryobj0 = "DROP TABLE HS_EXON;";

queryobj1 = "CREATE TABLE HS_EXON" + " (\n"
for i in range(len(infile_cols)):
	oldstr = infile_cols[i]
	newstr = oldstr.replace(" ", "_")
	newstr = newstr.replace("-", "_")
	newstr = newstr.replace(".", "_")
	newstr = newstr.replace(" ", "_")
	newstr = newstr.replace("(", "_")
	newstr = newstr.replace(")", "_")
	newstr = newstr.replace("", "_")
	if(i != (len(infile_cols) - 1)):
		query_set = newstr + " " + "TEXT ,\n"
	else:
		query_set = newstr + " " + "TEXT \n"
	queryobj1 = queryobj1 + query_set
queryobj1 = queryobj1 + ");\n"


queryobj2 = "COPY HS_EXON" + "\n"
queryobj2 = queryobj2 + "FROM '/data/salomonis2/NCI-R01/ONCObrowser/GeneModel/exonfin.csv'" + "\n"
queryobj2 = queryobj2 + "DELIMITER '#';"

queryobj3 = "CREATE UNIQUE INDEX " + "HS_EXON_btree_index ON " + "HS_EXON" + " USING btree(ENSEMBL_GENE_ID);"
querybox.append(queryobj0)
querybox.append(queryobj1)
querybox.append(queryobj2)
#querybox.append(queryobj3)

infilepath2 = "transcols.txt"
infile2 = open(infilepath2, "r")
infile_cols2 = next(infile2)
infile_cols2 = infile_cols2.rstrip()
infile_cols2 = infile_cols2.split("\t")
infile2.close()
print(len(infile_cols2))

queryobj4 = "DROP TABLE HS_TRANSCRIPT_ANNOT;";

queryobj5 = "CREATE TABLE HS_TRANSCRIPT_ANNOT" + " (\n"
for i in range(len(infile_cols2)):
	oldstr = infile_cols2[i]
	newstr = oldstr.replace(" ", "_")
	newstr = newstr.replace("-", "_")
	newstr = newstr.replace(".", "_")
	newstr = newstr.replace(" ", "_")
	newstr = newstr.replace("(", "_")
	newstr = newstr.replace(")", "_")
	newstr = newstr.replace("", "_")
	if(i != (len(infile_cols2) - 1)):
		query_set = newstr + " " + "TEXT ,\n"
	else:
		query_set = newstr + " " + "TEXT \n"
	queryobj5 = queryobj5 + query_set
queryobj5 = queryobj5 + ");\n"


queryobj6 = "COPY HS_TRANSCRIPT_ANNOT" + "\n"
queryobj6 = queryobj6 + "FROM '/data/salomonis2/NCI-R01/ONCObrowser/GeneModel/transfin.csv'" + "\n"
queryobj6 = queryobj6 + "DELIMITER '#';"

#queryobj7 = "CREATE UNIQUE INDEX " + "HS_TRANSCRIPT_ANNOT_btree_index ON " + "HS_TRANSCRIPT_ANNOT" + " USING btree(ENSEMBL_GENE_ID);"
querybox.append(queryobj4)
querybox.append(queryobj5)
querybox.append(queryobj6)
#querybox.append(queryobj7)

infilepath3 = "junccols.txt"
infile3 = open(infilepath3, "r")
infile_cols3 = next(infile3)
infile_cols3 = infile_cols3.rstrip()
infile_cols3 = infile_cols3.split("\t")
infile3.close()
print(len(infile_cols3))

queryobj7 = "DROP TABLE HS_JUNC;";

queryobj8 = "CREATE TABLE HS_JUNC" + " (\n"
for i in range(len(infile_cols3)):
	oldstr = infile_cols3[i]
	newstr = oldstr.replace(" ", "_")
	newstr = newstr.replace("-", "_")
	newstr = newstr.replace(".", "_")
	newstr = newstr.replace(" ", "_")
	newstr = newstr.replace("(", "_")
	newstr = newstr.replace(")", "_")
	newstr = newstr.replace("", "_")
	if(i != (len(infile_cols3) - 1)):
		query_set = newstr + " " + "TEXT ,\n"
	else:
		query_set = newstr + " " + "TEXT \n"
	queryobj8 = queryobj8 + query_set
queryobj8 = queryobj8 + ");\n"


queryobj9 = "COPY HS_JUNC" + "\n"
queryobj9 = queryobj9 + "FROM '/data/salomonis2/NCI-R01/ONCObrowser/GeneModel/juncfin.csv'" + "\n"
queryobj9 = queryobj9 + "DELIMITER '#';"

#queryobj7 = "CREATE UNIQUE INDEX " + "HS_TRANSCRIPT_ANNOT_btree_index ON " + "HS_TRANSCRIPT_ANNOT" + " USING btree(ENSEMBL_GENE_ID);"
querybox.append(queryobj7)
querybox.append(queryobj8)
querybox.append(queryobj9)
#querybox.append(queryobj7)


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
