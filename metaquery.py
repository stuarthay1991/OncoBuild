#make query

import preprocessingV3 as prep
import upload as U
def make(cancer):
	prep.moveTo(cancer.rootpath)
	colfile = open(("ToPostgres/metadata.txt.columns"), "r")
	cols = next(colfile)
	cols = cols.split(",")
	querybox = []
	queryfile = open("ToPostgres/metaquery.sql", "w")
	queryobj1 = "DROP TABLE " + cancer.name.replace("-", "_") + "_META;" + "\n"
	#print(len(cols))
	queryfile.write("CREATE TABLE " + cancer.name.replace("-", "_") + "_META" + " (\n")
	queryobj2 = "CREATE TABLE " + cancer.name.replace("-", "_") + "_META" + " (\n"
	for i in range(len(cols)):
		oldstr = cols[i]
		newstr = oldstr.replace("-", "_")
		newstr = newstr.replace(".", "_")
		newstr = newstr.replace(" ", "_")
		newstr = newstr.replace("*", "_")
		newstr = newstr.replace("/", "_")
		if(i != (len(cols) - 1)):
			query_set = newstr + " " + "TEXT ,\n"
		else:
			query_set = newstr + " " + "TEXT \n"
		queryfile.write(query_set)
		queryobj2 = queryobj2 + query_set;

	queryfile.write(")")
	queryobj2 = queryobj2 + ");"
	queryfile.write("\n")
	queryobj2 = queryobj2 + "\n"
	queryobj3 = "COPY " + cancer.name.replace("-", "_") + "_META" + "\n"
	queryfile.write("COPY " + cancer.name.replace("-", "_") + "_META" + "\n")
	queryobj3 = queryobj3 + "FROM '" + cancer.rootpath + "/ToPostgres/metadata.txt.pgr.csv'" + "\n"
	queryfile.write("FROM '" + cancer.rootpath + "/ToPostgres/metadata.txt.pgr.csv'" + "\n")
	queryobj3 = queryobj3 + "DELIMITER '#'" + "\n"
	queryfile.write("DELIMITER '#'" + "\n")
	queryobj3 = queryobj3 + "CSV HEADER;"
	queryfile.write("CSV HEADER;")
	#queryobj4 = "CREATE UNIQUE INDEX " + cancer.name.replace("-", "_") + "meta_btree_index ON " + cancer.name.replace("-", "_") + "_META" + " USING btree(uid);";
	querybox.append(queryobj1)
	querybox.append(queryobj2)
	querybox.append(queryobj3)
	#querybox.append(queryobj4)
	queryfile.close()
	U.sync(querybox)
