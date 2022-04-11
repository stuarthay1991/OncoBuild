import preprocessingV3 as prep
import upload as U
def sigQuery(cancer):
	prep.moveTo(cancer.rootpath)
	infilepath = "ToPostgres/oncosig.txt"
	infile = open(infilepath, "r")
	infile_cols = next(infile)
	infile_cols = infile_cols.rstrip()
	infile_cols = infile_cols.split("#")
	querybox = []
	queryobj1 = "DROP TABLE " + cancer.name.replace("-", "_") + "_SIGNATURE;" + "\n"
	queryfile = open("ToPostgres/oncosigquery.sql", "w")
	queryobj2 = "CREATE TABLE " + cancer.name.replace("-", "_") + "_SIGNATURE" + " (\n"
	queryfile.write("CREATE TABLE " + cancer.name.replace("-", "_") + "_SIGNATURE" + " (\n")
	for i in range(len(infile_cols)):
		oldstr = infile_cols[i]
		newstr = oldstr.replace("-", "_")
		newstr = newstr.replace(".", "_")
		newstr = newstr.replace("+", "positive_")
		newstr = newstr.replace(" ", "_")
		newstr = newstr.replace("(", "_")
		newstr = newstr.replace(")", "_")
		newstr = newstr.replace("", "_")
		if(i != (len(infile_cols) - 1)):
			query_set = newstr + " " + "TEXT ,\n"
		else:
			query_set = newstr + " " + "TEXT \n"
		queryfile.write(query_set)
		queryobj2 = queryobj2 + query_set

	queryfile.write(")\n")
	queryobj2 = queryobj2 + ");\n"
	queryfile.write("COPY " + cancer.name.replace("-", "_") + "_SIGNATURE" + "\n")
	queryobj3 = "COPY " + cancer.name.replace("-", "_") + "_SIGNATURE" + "\n"
	queryfile.write("FROM '" + cancer.rootpath + "/ToPostgres/oncosig.txt.pgr.csv'" + "\n")
	queryobj3 = queryobj3 + "FROM '" + cancer.rootpath + "/ToPostgres/oncosig.txt.pgr.csv'" + "\n"
	queryfile.write("DELIMITER '#'" + "\n")
	queryobj3 = queryobj3 + "DELIMITER '#'" + "\n"
	queryfile.write("CSV HEADER;")
	queryobj3 = queryobj3 + "CSV HEADER;"
	queryfile.close()
	queryobj4 = "CREATE UNIQUE INDEX " + cancer.name.replace("-", "_") + "siguid_btree_index ON " + cancer.name.replace("-", "_") + "_SIGNATURE" + " USING btree(uid);";

	querybox.append(queryobj1)
	querybox.append(queryobj2)
	querybox.append(queryobj3)
	querybox.append(queryobj4)
	U.sync(querybox)
	oncocolfile = open("ToPostgres/oncofields.txt", "w")
	writecolfile = "#".join(infile_cols)
	oncocolfile.write(writecolfile)
	oncocolfile.close()

	pgrfile = open("ToPostgres/oncosig.txt.pgr.csv", "w")
	try:
		while(True):
			infile_rows = next(infile)
			pgrfile.write(infile_rows)
	except:
		print("DONE!")
	pgrfile.close()
