def makeComparison(cancer):
	eventfile = open(cancer.eventspath, "r")
	metafile = open(cancer.metapath, "r")

	eventfile_line = next(eventfile)
	final_splitter = "EventAnnotation\t"
	new_one = eventfile_line.split(final_splitter)
	all_cols = new_one[1]
	all_cols = all_cols.split("\t")
	total_cols = str(len(all_cols))
	all_rows = []
	metafile_line = next(metafile)
	while(True):
                try:
                        metafile_line = next(metafile)
                        meta_tab_break = metafile_line.split("\t")
                        meta_row_index = meta_tab_break[0]
                        all_rows.append(meta_row_index)
                except:
                        break
	total_rows = str(len(all_rows))
	eventfile.close()
	metafile.close()
	print(("Total entries for clinical metadata: " + total_rows))
	print(("Total columns for events: " + total_cols))
	modified_cols = []
	for i in all_cols:
                k = i[0:12]
                modified_cols.append((k.upper()))
	modified_rows = []
	for i in all_rows:
                k = i[0:12]
                modified_rows.append((k.upper()))   
	t = set(modified_cols)
	j = set(modified_rows)
	if(len(modified_cols) > len(modified_rows)):
				y = j.intersection(t)
	else:
				y = t.intersection(j)
	print(("Total matches: ") + str(len(list(y))))
	print(t)
	print(j)