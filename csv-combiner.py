"""
Author: Anthony Cabrera-Lara
File: csv-combiner.py
Input: Minimum of one csv file and file name for output
"""
import csv
import pandas as pd
import sys
import os

class  Combiner:
    def __init__(self, list):
        self.validate_arguments(list)
        self.csv_files = list[1 : len(list)-1]
        self.destination = list[len(list)-1]
        self.column_names = self.generate_columns()
        self.generate_master_file()
        print(list[len(list) - 1] + " created")
    
    # print all of the input csv files that will be copied from
    def print_files(self):
        print(self.get_csv_files())
    
    # generates destination file and copies all data from input csv files
    def generate_master_file(self):
        # build master file
        with open(self.get_destination(), 'w') as master_file:
            csv_writer = csv.DictWriter(master_file, fieldnames=self.get_columns_names(), delimiter=",", quoting=csv.QUOTE_ALL)
            csv_writer.writeheader()

            # read all file inputs and read all rows to be copied
            for file in self.get_csv_files():
                with open(file, 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    
                    # read each line to handle all elements within row
                    for line in csv_reader:
                        
                        # build dictionary
                        new_row = line
                        
                        # if value is not provided for specific header associated element then input nothing
                        for column in self.get_columns_names():
                            if not column in new_row.keys():
                                new_row[column] = ""
                        
                        # get file name to be applied to dictionary
                        file_name = os.path.basename(file)
                        new_row["filename"] = file_name
                        
                        csv_writer.writerow(new_row)

    # reads columns from all files
    def generate_columns(self):
        column_names = []
        for file in self.get_csv_files():
            reader = pd.read_csv(file)
            for col in reader.columns:
                if not (col in column_names):
                    column_names.append(col)

        column_names.append("filename")
        return column_names

    # return list of columns
    def get_columns_names(self):
        return self.column_names

    # return list of input csv files
    def get_csv_files(self):
        return self.csv_files

    # return file name for destination of combined csv files
    def get_destination(self):
        return self.destination

    # validate all user arguments are valid
    def validate_arguments(self, user_arguments):
        is_valid = True
        if len(user_arguments) < 3:
            print("A minimum of 1 input csv file and a filename for output file is required")
            is_valid = False

        for i in range(1, len(user_arguments)-1):
            if not os.path.exists(user_arguments[i]):
                print(user_arguments[i] + " is not a valid file or is in wrong directory")
                is_valid = False

        if (not is_valid):
            raise Exception


# attempt to execute combination of CSV files
try:
    user_arguments = sys.argv
    combine = Combiner(sys.argv)

except:
    print("Unable to run " + user_arguments[0])