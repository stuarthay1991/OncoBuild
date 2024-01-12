import preprocessingV3 as prep
import upload as U

def makequery(rootdir):
	querybox = []
	createTableQueryStatement = "CREATE TABLE " + "cbioportalCancerStudies" + " (\n" + "ONCOSPLICE " + "TEXT ,\n" + "CBIOPORTAL " + "TEXT \n"
	createTableQueryStatement = createTableQueryStatement + ");"
	createTableQueryStatement = createTableQueryStatement + "\n"

	copyTableQueryStatement = "COPY " + "cbioportalCancerStudies" + "\n"
	copyTableQueryStatement = copyTableQueryStatement + "FROM '" + rootdir + "cbioportalCancerStudies.csv'" + "\n"
	copyTableQueryStatement = copyTableQueryStatement + "DELIMITER '#'" + "\n"
	copyTableQueryStatement = copyTableQueryStatement + "CSV HEADER;"
	querybox.append(createTableQueryStatement)
	querybox.append(copyTableQueryStatement)
	U.sync(querybox)

if __name__ == "__main__":
	makequery("/data/salomonis2/NCI-R01/ONCObrowser/")