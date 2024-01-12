import preprocessingV3 as prep
import upload as U

def makequery(rootpath):
        pathtomake = rootpath + "/Completed/"
        querybox = []
        queryobj1 = "DROP TABLE SUPERSIG;" + "\n"
        queryobj2 = "CREATE TABLE SUPERSIG" + " (\n"
        queryobj2 = queryobj2 + "cancer_name TEXT ,\nsignature_name TEXT ,\nfirstjunc TEXT ,\nUID TEXT ,\nEvent_Direction TEXT ,\nClusterID TEXT ,\nEventAnnotation TEXT \n"
        queryobj2 = queryobj2 + ");"
        queryobj2 = queryobj2 + "\n"
        queryobj3 = "COPY SUPERSIG" + "\n"
        queryobj3 = queryobj3 + "FROM '" + pathtomake + "supereventtable.csv'" + "\n"
        queryobj3 = queryobj3 + "DELIMITER '#'" + "\n"
        queryobj3 = queryobj3 + "CSV HEADER;"
        queryobj4 = "CREATE INDEX supersig_hash_index ON supersig USING HASH (firstjunc);";
        queryobj5 = "CREATE INDEX supersig_hash_index2 ON supersig USING HASH (signature_name);";
        queryobj6 = "CREATE INDEX supersig_hash_index3 ON supersig USING HASH (Event_Direction);";
        queryobj7 = "CREATE INDEX supersig_hash_index4 ON supersig USING HASH (UID);";
        print("made a table")
        querybox.append(queryobj1)
        querybox.append(queryobj2)
        querybox.append(queryobj3)
        querybox.append(queryobj4)
        querybox.append(queryobj5)
        querybox.append(queryobj6)
        querybox.append(queryobj7)
        U.sync(querybox)
