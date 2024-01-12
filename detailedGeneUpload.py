import preprocessingV3 as prep
import upload as U
def makequery(cancer):
	prep.moveTo(cancer.rootpath)
	queryfile = open("ToPostgres/detailedGeneQuery.sql", "w")
	queryfile.write("CREATE TABLE " + cancer.name.replace("-", "_") + "_FULLDEGENE" + " (\n")
	querybox = []
	#queryobj1 = "DROP TABLE " + cancer.name.replace("-", "_") + "_FULLDEGENE;" + "\n"
	queryobj2 = "CREATE TABLE " + cancer.name.replace("-", "_") + "_FULLDEGENE" + " (\n"
	queryobj2 = queryobj2 + "signature_name TEXT ,\nGeneID TEXT ,\nSystemCode TEXT ,\nLogFold TEXT ,\nrawp TEXT ,\nadjp TEXT ,\nSymbol TEXT ,\navg_Self TEXT ,\navg_Others TEXT \n"
	queryfile.write(");")
	queryobj2 = queryobj2 + ");"
	queryfile.write("\n")
	queryobj2 = queryobj2 + "\n"
	queryfile.write("COPY " + cancer.name.replace("-", "_") + "_FULLDEGENE" + "\n")
	queryobj3 = "COPY " + cancer.name.replace("-", "_") + "_FULLDEGENE" + "\n"
	queryfile.write("FROM '" + cancer.rootpath + "/ToPostgres/detailedDE.csv'" + "\n")
	queryobj3 = queryobj3 + "FROM '" + cancer.rootpath + "/ToPostgres/detailedDE.csv'" + "\n"
	queryfile.write("DELIMITER '#'" + "\n")
	queryobj3 = queryobj3 + "DELIMITER '#'" + "\n"
	queryfile.write("CSV HEADER;")
	queryobj3 = queryobj3 + "CSV HEADER;"
	queryfile.close()
	print("made a table")
	#querybox.append(queryobj1)
	querybox.append(queryobj2)
	querybox.append(queryobj3)
	U.sync(querybox)
