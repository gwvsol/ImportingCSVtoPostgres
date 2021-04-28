from csv import DictReader

file_csv = "coords.csv"

# open file in read mode
with open(file_csv, 'r') as read_obj:
    # pass the file object to DictReader() to get the DictReader object
    csv_dict_reader = DictReader(read_obj)
    # iterate over each line as a ordered dictionary
    for row in csv_dict_reader:
        # row variable is a dictionary that represents a row in csv
        print(row)