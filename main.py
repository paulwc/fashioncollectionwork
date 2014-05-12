import csv
import os
import fnmatch

directory = os.getcwd()
# pattern = '*.jpg'

ident = {}
files_dict = {}
match_count = 0

# dump images into an array
for root, dirs, files in os.walk(directory):
    # for filename in fnmatch.filter(files, pattern):
    for filename in files:
        if filename.endswith(('.jpg', '.jpeg', '.gif', '.png', '.tiff', '.tif')):
            files_dict[filename] = os.path.join(root, filename)

with open('omeka.csv') as f, open('omeka_with_images_no_spaces.csv', 'wb') as csvwritefile:
    csvreader = csv.DictReader(f)
    fieldnames = csvreader.fieldnames + ['Filenames']

    csvwriter = csv.DictWriter(csvwritefile, fieldnames)
    csvwriter.writeheader()


    for row in csvreader:
        # process row
        row['Accession Number'] = row['Accession Number'].replace(" ", "_")
        acc_num = row['Accession Number']
        filenames = set()
        for key, value in files_dict.items():
            if key.find(acc_num) != -1:
                filenames.add(value)
                match_count += 1
#                 files_dict.pop(key) # remove picture from dictionary
        filenameString = ','.join(str(x) for x in filenames)
#         print (filenames)

        csvwriter.writerow(dict(row, Filenames=filenameString))

print ("Matched " + str(match_count) + " items")
