import psycopg2
import traceback
import os

infilepath = "/data/salomonis2/NCI-R01/ONCObrowser/Gtex/gtex_cols.txt"
infile = open(infilepath, "r")
infile_cols = next(infile)
infile_cols = infile_cols.rstrip()
infile_cols = infile_cols.split("\t")
querybox = []
print(len(infile_cols))

queryobj0 = "DROP TABLE GTEX;";

queryobj1 = "CREATE TABLE GTEX" + " (\n"
for i in range(len(infile_cols)):
	oldstr = infile_cols[i]
	newstr = oldstr.replace("-", "_")
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


queryobj2 = "COPY GTEX" + "\n"
queryobj2 = queryobj2 + "FROM '/data/salomonis2/NCI-R01/ONCObrowser/Gtex/gtex_matrix.txt.csv'" + "\n"
queryobj2 = queryobj2 + "DELIMITER '#';"

queryobj3 = "CREATE UNIQUE INDEX " + "GTEXuid_btree_index ON " + "GTEX" + " USING btree(UID);"
querybox.append(queryobj0)
querybox.append(queryobj1)
querybox.append(queryobj2)
querybox.append(queryobj3)

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

