#make query

import preprocessingV3 as prep
import upload as U
def makequery(cancer):
	prep.moveTo(cancer.rootpath)
	colfile = open(("ToPostgres/events.columns"), "r")
	cols = next(colfile)
	cols = cols.split(",")
	queryfile = open("ToPostgres/splicequery.sql", "w")
	print(len(cols))
	queryfile.write("CREATE TABLE " + cancer.name.replace("-", "_") + "_SPLICE" + " (\n")
	querybox = []
	queryobj1 = "DROP TABLE " + cancer.name.replace("-", "_") + "_SPLICE;" + "\n"
	queryobj2 = "CREATE TABLE " + cancer.name.replace("-", "_") + "_SPLICE" + " (\n"
	for i in range(len(cols)):
		oldstr = cols[i]
		newstr = oldstr.replace("-", "_")
		newstr = newstr.replace(".", "_")
		newstr = newstr.replace(" ", "_")
		if(i != (len(cols) - 1)):
			query_set = newstr + " " + "TEXT ,\n"
		else:
			query_set = newstr + " " + "TEXT \n"
		queryfile.write(query_set)
		queryobj2 = queryobj2 + query_set

	queryfile.write(");")
	queryobj2 = queryobj2 + ");"
	queryfile.write("\n")
	queryobj2 = queryobj2 + "\n"
	queryfile.write("COPY " + cancer.name.replace("-", "_") + "_SPLICE" + "\n")
	queryobj3 = "COPY " + cancer.name.replace("-", "_") + "_SPLICE" + "\n"
	queryfile.write("FROM '" + cancer.rootpath + "/ToPostgres/events.pgr.csv'" + "\n")
	queryobj3 = queryobj3 + "FROM '" + cancer.rootpath + "/ToPostgres/events.pgr.csv'" + "\n"
	queryfile.write("DELIMITER '#'" + "\n")
	queryobj3 = queryobj3 + "DELIMITER '#'" + "\n"
	queryfile.write("CSV HEADER;")
	queryobj3 = queryobj3 + "CSV HEADER;"
	queryobj4 = "CREATE UNIQUE INDEX " + cancer.name.replace("-", "_") + "uidsplice_btree_index ON " + cancer.name.replace("-", "_") + "_SPLICE" + " USING btree(uid);";
	queryobj5 = "CREATE UNIQUE INDEX " + cancer.name.replace("-", "_") + "panuidsplice_btree_index ON " + cancer.name.replace("-", "_") + "_SPLICE" + " USING btree(pancanceruid);";
	queryfile.close()
	querybox.append(queryobj1)
	querybox.append(queryobj2)
	querybox.append(queryobj3)
	querybox.append(queryobj4)
	querybox.append(queryobj5)
	U.sync(querybox)
