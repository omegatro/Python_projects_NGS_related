import csv
import os
import time


def bc_list_generator(file_name):
    reader = csv.reader(open(file_name, 'r'))
    bc_list = []

    for row_1 in reader:
        bc_list.append([row_1[0], row_1[1]])
    return bc_list


def barcode_compatibility_test(list_of_barcodes_to_check):
    nucleotide_counter = 0
    barcode_compatibility_data = []
    dcr_pos_in_bc_seq = 0
    bc_list_length = len(list_of_barcodes_to_check)

    while dcr_pos_in_bc_seq <= len(list_of_barcodes_to_check[0][1]) - 1:
        if nucleotide_counter == len(list_of_barcodes_to_check[0][1]):
            nucleotide_counter = 0

        bc_list_counter = 0
        a_count = 0
        t_count = 0
        c_count = 0
        g_count = 0

        while bc_list_counter <= len(list_of_barcodes_to_check) - 1:
            if list_of_barcodes_to_check[bc_list_counter][1][nucleotide_counter] == "A":
                a_count += 1 / bc_list_length
            elif list_of_barcodes_to_check[bc_list_counter][1][nucleotide_counter] == "T":
                t_count += 1 / bc_list_length
            elif list_of_barcodes_to_check[bc_list_counter][1][nucleotide_counter] == "C":
                c_count += 1 / bc_list_length
            elif list_of_barcodes_to_check[bc_list_counter][1][nucleotide_counter] == "G":
                g_count += 1 / bc_list_length
            bc_list_counter += 1

        nucleotide_counter += 1
        barcode_compatibility_data.append([dcr_pos_in_bc_seq + 1, a_count, t_count, g_count, c_count])
        dcr_pos_in_bc_seq += 1
    return barcode_compatibility_data


def barcode_comp_data_editor(bc_comp_data, list_of_bc):
    data_header = ["Nt_nr", "A", "T", "G", "C", "B_C ID", "1", "2", "3", "4", "5", "6", "7", "8",
                   "9", "10", "B_C SEQ", "BC_Total: " + str(len(list_of_bc))]
    bc_comp_data.insert(0, data_header)

    l_1 = 0
    k_1 = 1
    while k_1 <= len(bc_comp_data) - 1:
        if l_1 > len(list_of_bc) - 1:
            break
        bc_comp_data[k_1].append(list_of_bc[l_1][0])

        for nucleotide in list_of_bc[l_1][1]:
            bc_comp_data[k_1].append(nucleotide)
        bc_comp_data[k_1].append(list_of_bc[l_1][1])
        l_1 += 1
        k_1 += 1

    if len(list_of_bc) > 10:
        m_1 = len(list_of_bc)
        difference = m_1 - len(bc_comp_data) + 1

        while m_1 >= len(bc_comp_data) - difference:
            list_to_app = ["", "", "", "", "", list_of_bc[k_1 - 1][0]]

            for nt in list_of_bc[k_1 - 1][1]:
                list_to_app.append(nt)
            list_to_app.append(list_of_bc[k_1 - 1][1])
            bc_comp_data.append(list_to_app)
            m_1 -= 1
            k_1 += 1
    # Case when there are < 10 barcodes is not covered.
    return bc_comp_data


def bc_writer(format_bc_data, bc_table_source):
    with open('barcode_compatibility_report.csv', 'w', newline='') as pooled_file:
        writer1 = csv.writer(pooled_file)
        for row in format_bc_data:
            writer1.writerow(row)
        print("The barcodes to compare are taken from " + bc_table_source + " file.")
        print("The file with barcode compatibility report was created.")
        print("The path to the report file and the barcode source file is: ")
        print(str(os.getcwd()))


bc_file_name = "Barcodes_to_check.csv"
bc_compatibility_data = barcode_compatibility_test(bc_list_generator(bc_file_name))
barcode_list = bc_list_generator(bc_file_name)
formatted_bc_compatibility_data = barcode_comp_data_editor(bc_compatibility_data, barcode_list)
bc_writer(formatted_bc_compatibility_data, bc_file_name)

user_input_check = False
while not user_input_check:
    user_input = input("Type y to end the script:")
    if user_input == "y":
        user_input_check = True
        print("Have a nice day =)")
        time.sleep(1)
