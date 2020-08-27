import codecs
from bs4 import BeautifulSoup
import ast
import csv
import os


def summary_report_to_csv(html_filename, csv_name):
    html = codecs.open(str(html_filename), "r", "utf-8")
    # Reading an html file from the current working directory and assigning result to the variable.
    souped_info = BeautifulSoup(html, 'html.parser')
    # Parsing the html file using BeautifulSoup module and assigning the result to the variable.
    javascript = souped_info.find_all(type="text/javascript")
    # Looking for the javascript part of the html in the parsed version of the file and assigning it to the variable.
    # At this point the javascript portion that we are interested is stored as module-specific type.

    summary_table_count = str(javascript).count("var summaryTable")
    info_table_count = str(javascript).count("var bioTable")
    # Looking for and counting the number of (to ensure uniqueness) concrete tables...
    # ...that are stored in javascript variables.
    # String methods are applied, so the javascript code must be converted to type string first.

    report_list = []
    # The data from parsed tables will be stored as sub-lists in the report_list.

    if summary_table_count == 1 and info_table_count == 1:
        start = str(javascript).find('var summaryTable')
        end = str(javascript).find("']];")
        # Looking for the beginning and the end of the table of interest.
        # Later this information is used to extract tables as substrings of javascript code.

        start_inf = str(javascript).find('var bioT')
        end_inf = str(javascript).find("']];", start_inf)
        # Repeating the boundary search for the second table.
        # As .find method finds the starting index of only the first substring it encounters,
        # the interval of search should be specified by including the substring that marks the beginning of the table.

        summary_table = str(javascript)[start:end+2]
        info_table = str(javascript)[start_inf:end_inf+2]
        # Extracting the required tables as substrings from string of javascript code.

        add_len = len('var summaryTable = ')
        summary_table = summary_table[add_len+1:]
        add_len_inf = len('var bioTable = ')
        info_table = info_table[add_len_inf+1:]
        # Additional formatting of the resulting strings with the table information...
        # ... to adjust it for further type change to list.

        sum_table_list = ast.literal_eval(summary_table)
        info_table_list = ast.literal_eval(info_table)
        # Changing the types of table strings to lists.

        for data in info_table_list:
            if data[0] == 'Machine ID':
                report_list.append(data)
            elif data[0] == 'Sequence Date':
                report_list.append(data)
            elif data[0] == 'Reagent ID':
                report_list.append(data)
            elif data[0] == 'Barcode File':
                report_list.append(data)

        for data in sum_table_list:
            if data[0] == 'TotalReads(M)':
                report_list.append(data)
            elif data[0] == 'Q30(%)':
                report_list.append(data)
            elif data[0] == 'SplitRate(%)':
                report_list.append(data)
            elif data[0] == 'ESR(%)':
                report_list.append(data)
    # Extracting the required information from the list of table values produced in the previous step.
    # The resulting data are stored in the report_list.

    with open(str(csv_name), 'w', newline='') as file:
        writer = csv.writer(file)
        for element in report_list:
            writer.writerow(element)
    # Creating a .csv file in the current working directory...
    # ... and adding each element of the report_list to this file as a new row.


def clear_csv(directory_path):
    os.chdir(directory_path)
    list_of_files = os.listdir(os.getcwd())
    list_of_csv_local = []
    for n in list_of_files:
        if '.csv' in n:
            list_of_csv_local.append(n)
    for file in list_of_csv_local:
        os.remove(file)


def massive_report_to_csv(wdpath):
    clear_csv(wdpath)
    os.chdir(wdpath)
    # Setting the current working directory to the path given when the function is called.

    if os.path.exists('pooled_summary_report.csv'):
        os.remove('pooled_summary_report.csv')
    # Checking if the resulting file from previous run is still in the working directory...
    # ... and deleting it, if it's still there.

    list_of_files = os.listdir(wdpath)
    # Getting a list of all file names in the current working directory.

    list_of_html = []
    for file_name in list_of_files:
        if '.html' in file_name:
            list_of_html.append(file_name)
    # Getting a list of .html file names from the list of all file names.

    for name in list_of_html:
        summary_report_to_csv(name, str.replace(name, '.html', '') + '.csv')
    # Collecting data from each html file in the list_of_html and adding it to the csv file.
    # One csv file corresponds to one html file.

    list_of_files = os.listdir(wdpath)
    # Updating the list_of_files in the current working directory after the .csv files were created.

    list_of_csv_local = []
    for n in list_of_files:
        if '.csv' in n:
            str.replace(n, '.html', '')
            list_of_csv_local.append(n)
    # Checking if the csv files were created, removing .html part from the file name...
    # ... and creating an up-to-date list of .csv files in the current working directory.

    return list_of_csv_local
    # The function returns the list of .csv file names...
    # ... that will be used for combining the multiple generated .csv files into one .csv file.


def csv_pooler(csv_list):
    # The function gets list of csv files as an input from the massive_report_to_csv() function.

    csv_content_list = []
    # Creating a list in which the contents of .csv files will be stored.
    # This will become a list of lists,
    # where each sub-list corresponds to 1 column in 1 .csv file.

    for csv_local in csv_list:
        reader = csv.reader(open(csv_local, 'r'))
        list_1 = []
        list_2 = []
        for row in reader:
            list_1.append(row[0])
            list_2.append(row[1])
        csv_content_list.append(list_1)
        csv_content_list.append(list_2)
    # Each file that is in the csv_list is read, and its contents are saved in the temporary list named reader.
    # After the file is fully processed, the contents of each sublist from the reader list (row of .csv) is divided.
    # First element, corresponding to the 1st column of a given file, is saved in list_1.
    # The contents of the 2nd column are saved in list_2.
    # Both lists are then added to the csv_content_list as columns of the combined .csv file.
    # reader, list_1 and list_2 are reinitialised for each new .csv file.

    i = 0
    j = 0
    pooled_list = []
    while j <= len(csv_content_list[0])-1:
        pool = []
        for list_iter in csv_content_list:
            pool.append(list_iter[i])
        pooled_list.append(pool)
        i += 1
        j += 1
    # In order to correctly write the data into combined .csv file,...
    # ... the values that go into one row should be stored as one list.
    # The double loop above transforms the sub-lists of csv_content_list (that correspond to columns of .csv)...
    # ... into sub-lists that correspond to the rows of .csv, and adds it to the new list.
    # The conversion can be viewed as follows:
    # [[1, 2, 3, 4], [5, 6, 7, 8]] --> [[1, 5], [2, 6], [3, 7], [4, 8]]

    with open('pooled_summary_report.csv', 'w', newline='') as pooled_file:
        writer1 = csv.writer(pooled_file)
        for pool in pooled_list:
            writer1.writerow(pool)
    # The data stored in the pooled_list are added to the new, combined .csv file.


csv_pooler(massive_report_to_csv('C:\\Users\\omega\\PycharmProjects\\PythonLearn101\\Test_files\\Summary_reports'))
# The nested function call to initiate the program; wdpath variable of massive_report_to_csv...
# ... should be changed according to the location of files.
