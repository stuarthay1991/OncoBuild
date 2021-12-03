#View components of large files

import preprocessing as prep

prep.moveTo(prep.testingdatadir)

file_to_view = open(prep.objects[1], "r")
num_rows = int(prep.objects[2])

count = 0
for line in file_to_view:
    if(count > num_rows):
        break
    else:
        print(line)
        count = count + 1
