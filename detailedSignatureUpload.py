import preprocessingV3 as prep
import upload as U
def makequery(cancer):
	prep.moveTo(cancer.rootpath)
	queryfile = open("ToPostgres/detailedSigQuery.sql", "w")
	queryfile.write("CREATE TABLE " + cancer.name.replace("-", "_") + "_FULLSIG" + " (\n")
	querybox = []
	queryobj1 = "DROP TABLE " + cancer.name.replace("-", "_") + "_FULLSIG;" + "\n"
	queryobj2 = "CREATE TABLE " + cancer.name.replace("-", "_") + "_FULLSIG" + " (\n"
	queryobj2 = queryobj2 + "signature_name TEXT ,\nUID TEXT ,\nEvent_Direction TEXT ,\nClusterID TEXT ,\nEventAnnotation TEXT ,\nCoordinates TEXT ,\nProteinPredictions TEXT ,\ndPSI TEXT ,\nrawp TEXT ,\nadjp TEXT ,\navg_Others TEXT \n"

	queryfile.write(");")
	queryobj2 = queryobj2 + ");"
	queryfile.write("\n")
	queryobj2 = queryobj2 + "\n"
	queryfile.write("COPY " + cancer.name.replace("-", "_") + "_FULLSIG" + "\n")
	queryobj3 = "COPY " + cancer.name.replace("-", "_") + "_FULLSIG" + "\n"
	queryfile.write("FROM '" + cancer.rootpath + "/ToPostgres/detailedSignature.csv'" + "\n")
	queryobj3 = queryobj3 + "FROM '" + cancer.rootpath + "/ToPostgres/detailedSignature.csv'" + "\n"
	queryfile.write("DELIMITER '#'" + "\n")
	queryobj3 = queryobj3 + "DELIMITER '#'" + "\n"
	queryfile.write("CSV HEADER;")
	queryobj3 = queryobj3 + "CSV HEADER;"
	queryfile.close()
	print("made a table")
	queryobj4 = "CREATE INDEX " + cancer.name.replace("-", "_") + "_FULLSIG" + "supersig_hash_index ON " + cancer.name.replace("-", "_") + "_FULLSIG" + " USING HASH (EventAnnotation);";
	queryobj5 = "CREATE INDEX " + cancer.name.replace("-", "_") + "_FULLSIG" + "supersig_hash_index2 ON " + cancer.name.replace("-", "_") + "_FULLSIG" + " USING HASH (signature_name);";
	queryobj6 = "CREATE INDEX " + cancer.name.replace("-", "_") + "_FULLSIG" + "supersig_hash_index3 ON " + cancer.name.replace("-", "_") + "_FULLSIG" + " USING HASH (Event_Direction);";
	queryobj7 = "CREATE INDEX " + cancer.name.replace("-", "_") + "_FULLSIG" + "supersig_hash_index4 ON " + cancer.name.replace("-", "_") + "_FULLSIG" + " USING HASH (UID);";
	querybox.append(queryobj1)
	querybox.append(queryobj2)
	querybox.append(queryobj3)
	querybox.append(queryobj4)
	querybox.append(queryobj5)
	querybox.append(queryobj6)
	querybox.append(queryobj7)
	U.sync(querybox)
