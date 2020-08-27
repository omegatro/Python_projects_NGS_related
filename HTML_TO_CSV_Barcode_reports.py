import codecs
from bs4 import BeautifulSoup
import ast
import csv
import os

# Comments for sections that are copied from HTML_TO_CSV_Summary_reports.py are omitted.


def barcode_report_to_csv(html_filename, csv_name):
    html = codecs.open(html_filename, "r", "utf-8")
    # Opens the html file for reading.
    souped_info = BeautifulSoup(html, 'html.parser')
    # Parses opened html file, producing a bs4 type iterable object.
    javascript = souped_info.find_all(type="text/javascript")
    # Searches for js part in the html file and saves it as a bs4 type iterable object.

    report_list = []

    start = str(javascript).find('var reportTitle')
    end = str(javascript).find('";', start)
    # Finding the title of a barcode report that contains flowcell id, barcode number and lane identifier.

    barcode_id = str(javascript)[start:end+2]
    add_len = len('var reportTitle = ')
    barcode_id = barcode_id[add_len + 1:-2]
    # Formatting barcode report title to contain only required information (flowcell id, lane id, barcode number).

    start_1 = str(javascript).find('var summaryTable')
    end_1 = str(javascript).find("']];")

    summary_table = str(javascript)[start_1:end_1 + 2]

    add_len = len('var summaryTable = ')
    summary_table = summary_table[add_len + 1:]

    sum_table_list = list(ast.literal_eval(summary_table))
    # ast.literal_eval() converts a string containing "," as delimiters into a list.
    sum_table_list.insert(0, [barcode_id, ''])

    for data in sum_table_list:
        if 'Analysis Report of' in data[0]:
            report_list.append([data[0][len('Analysis Report of')+1:], data[1]])
        elif data[0] == 'Q30(%)':
            report_list.append(data)
        # elif data[0] == 'TotalReads(M)':
        #     report_list.append(data)
        # Total reads before Q30 in pooled report.

    for data in sum_table_list:
        if data[0] == 'TotalReads(M)':
            report_list.append(data)
    # Q30 before Total reads in pooled report.

    with open(str(csv_name), 'w', newline='') as file:
        writer = csv.writer(file)
        for element in report_list:
            writer.writerow(element)


def clear_csv(directory_path):
    os.chdir(directory_path)
    list_of_files = os.listdir(os.getcwd())
    list_of_csv_local = []
    for n in list_of_files:
        if '.csv' in n:
            list_of_csv_local.append(n)
    for file in list_of_csv_local:
        os.remove(file)
# The function clears all .csv files from the specified directory.


def massive_report_to_csv(wdpath):
    clear_csv(wdpath)
    # Removing any .csv file present in current working directory,...
    # ... to ensure that no interference comes from data in old files.

    os.chdir(wdpath)

    list_of_files = os.listdir(wdpath)

    list_of_html = []
    for file_name in list_of_files:
        if '.html' in file_name:
            list_of_html.append(file_name)

    for name in list_of_html:
        barcode_report_to_csv(name, str.replace(name, '.html', '') + '.csv')

    list_of_files = os.listdir(wdpath)

    list_of_csv_local = []
    for n in list_of_files:
        if '.csv' in n:
            str.replace(n, '.html', '')
            list_of_csv_local.append(n)

    return list_of_csv_local


def csv_pooler(csv_list):
    csv_content_list = []

    for csv_local in csv_list:
        reader = csv.reader(open(csv_local, 'r'))
        list_1 = []
        list_2 = []
        for row in reader:
            list_1.append(row[0])
            list_2.append(row[1])
        csv_content_list.append(list_1)
        csv_content_list.append(list_2)

    csv_content_list[1][0] = csv_content_list[0][0]
    csv_content_list[0][0] = 'Barcode ID'
    # Formatting the csv_content_list so that first item in the list is the header with...
    # ... 'Barcode ID', 'Total Reads(M)' and 'Q30%' sections.

    i = 2
    while i <= len(csv_content_list)-1:
        if divmod(i, 2) != 0:
            csv_content_list[i+1][0] = csv_content_list[i][0]
            csv_content_list.remove(csv_content_list[i])
        i += 1
    # Formatting the csv_content_list so that each row after the 1st contains...
    # ... Barcode ID value, Total Reads(M) value and Q30% value specific for each sample/barcode number.

    with open('pooled_barcode_report.csv', 'w', newline='') as pooled_file:
        writer1 = csv.writer(pooled_file)
        for row in csv_content_list:
            writer1.writerow(row)


csv_pooler(massive_report_to_csv(''))
