import csv
# import datetime
import itertools
import os
import time
import sys


def clear_pools(directory_path, name='Pool'):
    os.chdir(directory_path)
    list_of_files = os.listdir(os.getcwd())
    list_of_csv_local = []
    for n in list_of_files:
        if name in n:
            list_of_csv_local.append(n)
    for file in list_of_csv_local:
        os.remove(file)


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


def bc_generator_call():
    list_of_barcodes = bc_list_generator("Barcodes_library.csv")
    print("There are " + str(len(list_of_barcodes)) + " bar codes in the library you provided.")
    pool_size = input("Enter the number of bar codes you need for the pool (must be at least 4), or type n to"
                      " exit the script: ")
    if pool_size == "n":
        sys.exit("The script will close.")
    elif int(pool_size) < 4:
        while int(pool_size) < 4:
            print("Pool size must be bigger than 3.")
            bc_generator_call()
    else:
        return [list_of_barcodes, pool_size]


def get_barcode_combinations(pool_length, list_of_barcodes_1, report=1):
    barcode_comb = itertools.combinations(list_of_barcodes_1, pool_length)
    h = 0
    for subset in barcode_comb:
        bc_test_values = barcode_compatibility_test(subset)
        i_l_v = True
        o_l_v = True
        h += 1
        if report == 1:
            print("Number of combination checked: " + str(h))
        for i in range(10):
            for j in range(1, 5):
                if bc_test_values[i][j] < 0.12:
                    i_l_v = False
                    break
            if not i_l_v:
                o_l_v = False
                break
        if o_l_v:
            return subset
        else:
            continue


def bc_comp_rep_printer(barcode_combination, file_name=""):
    if barcode_combination is not None:
        compatible_barcodes = list(barcode_combination)
        bc_comp_results = barcode_compatibility_test(compatible_barcodes)
        bc_comp_results.insert(0, ["Nt Nr", "A", "T", "G", "C"])
        compatible_barcodes.insert(0, ["BC ID", "BC SEQ"])
        for row in bc_comp_results:
            compatible_barcodes.append(row)

        with open("Pool #" + str(file_name) + ".csv", 'w', newline='') as pooled_file:
            writer1 = csv.writer(pooled_file)
            if type(compatible_barcodes) is not None:
                for row_0 in compatible_barcodes:
                    writer1.writerow(row_0)
                print("The file with bar codes for the pool have been created.")
                print("The path to the file is: " + str(os.getcwd()))

    else:
        print("No compatible barcodes are available from this library with selected pool size.")
        time.sleep(5)


# bc_generator = bc_generator_call()
# # BC_list generated
# pooled_barcodes = get_barcode_combinations(int(bc_generator[1]), bc_generator[0])
# # list of pooled barcodes generated
# bc_comp_rep_printer(get_barcode_combinations(int(bc_generator[1]), bc_generator[0]))


def barcode_list_renewer(bc_list, bc_pool):
    for row in bc_pool:
        for row_1 in bc_list:
            if row == row_1:
                bc_list.remove(row_1)
    return bc_list


def pool_generator(number_of_pools_to_get):
    bc_generator = bc_generator_call()
    pool_size = int(bc_generator[1])
    pooled_barcodes = list(get_barcode_combinations(pool_size, bc_generator[0], 0))
    bc_comp_rep_printer(get_barcode_combinations(pool_size, bc_generator[0]), str(1))
    for item in pooled_barcodes:
        for item_1 in bc_generator[0]:
            if item == item_1:
                bc_generator[0].remove(item_1)
    for i in range(0, number_of_pools_to_get-1):
        added_barcodes = list(get_barcode_combinations(pool_size, bc_generator[0], 0))
        pooled_barcodes = pooled_barcodes + added_barcodes
        for item in pooled_barcodes:
            for item_1 in bc_generator[0]:
                if item == item_1:
                    bc_generator[0].remove(item_1)
        bc_comp_rep_printer(get_barcode_combinations(pool_size, bc_generator[0]), str(i+2))


clear_pools(os.getcwd())
number_of_pools = int(input("Enter the number of pools you need: "))
if number_of_pools == 0:
    while number_of_pools == 0:
        print("Pool number can't be 0.")
        number_of_pools = int(input("Enter the number of pools you need: "))
    pool_generator(number_of_pools)
else:
    pool_generator(number_of_pools)
    user_input = input("Type n to quit the script: ")
while user_input != "n":
    user_input = input("Type n to quit the script: ")


# Add a recursive function call to ask for new number of barcodes in the pull.

# Below is the code used to get the time it takes to run the code in seconds.
# start_time = datetime.datetime.now()

# Insert the code you want to test here.

# end_time = datetime.datetime.now()
# time_diff = (end_time - start_time)
# execution_time = time_diff.total_seconds() * 1000
#
# print(execution_time)
