import csv
import os
import re
import sys


def folder_path_request():
    folder_path_to_check = input("Enter the path you want to check or type n to quit the script: ")
    folder_path_to_check = re.escape(folder_path_to_check)
    print(folder_path_to_check)
    # Adjusts the windows format path to the python format path.
    if folder_path_to_check == "n":
        sys.exit("The script is closing.")
    #   Stops the script execution.
    elif not os.path.exists(folder_path_to_check):
        print("The path doesn't exist.")
        folder_path_request()
    #   Recursively invites the user to enter valid path.
    else:
        print("The folder path to scan is: " + folder_path_to_check)
        list_of_folders = [f.path for f in os.scandir(folder_path_to_check) if f.is_dir()]
        list_of_files = []
        [list_of_files.append(os.listdir(path)) for path in list_of_folders]
        # Scans for files in the folders to be deleted.
        return folder_path_to_check
        #    Recursively invites the user to enter valid path.


def gz_searcher(folder_to_scan):
    list_of_folders = [f.path for f in os.scandir(folder_to_scan) if f.is_dir()]
    lists_of_file_names = []
    [lists_of_file_names.append(os.listdir(path)) for path in list_of_folders]
    gz_counter = 0
    gz_list_final = []
    for file_name in lists_of_file_names:
        for name in file_name:
            if ".gz" in name and "md5" not in name:
                gz_list_final.append(name)
                gz_counter += 1
    print("{} gz files were found.".format(gz_counter))
    return gz_list_final, gz_counter


def md5_searcher(folder_to_scan):
    list_of_folders = [f.path for f in os.scandir(folder_to_scan) if f.is_dir()]
    lists_of_file_names = []
    [lists_of_file_names.append(os.listdir(path)) for path in list_of_folders]
    md5_counter = 0
    md5_list_final = []
    for file_name in lists_of_file_names:
        for name in file_name:
            if "md5" in name:
                md5_list_final.append(name)
                md5_counter += 1
    print("{} md5 files were found.".format(md5_counter))
    return md5_list_final, md5_counter





def bc_list_generator(current_dir):
    os.chdir(current_dir)
    reader = csv.reader(open("Barcode_list_csv.csv", 'r'))
    bcs_list = []
    for row in reader:
        bcs_list.append(row[0])
    return bcs_list


def bc_filter(bc_list_md5, bc_list_gz):
    filtered_bcds_md5 = []
    for element in bc_list_md5:
        filtered_bcds_md5.append(element[0:-12])

    filtered_bcds_gz = []
    for element in bc_list_gz:
        filtered_bcds_gz.append(element[0:-8])
    filtered_bcds_gz = list(set(filtered_bcds_gz))
    return filtered_bcds_md5, filtered_bcds_gz


def data_check(bcd_list, filtered_bcs_md5_f, filtered_bcs_gz_f):
    bc_boolean_samples_to_data_md5 = {}
    for element in bcd_list:
        if element in filtered_bcs_md5_f:
            bc_boolean_samples_to_data_md5[element] = True
        else:
            bc_boolean_samples_to_data_md5[element] = False
    # [print(pair) for pair in bc_boolean_samples_to_data_md5.items()]

    bc_boolean_data_to_samples_md5 = {}
    for element in filtered_bcs_md5_f:
        if element in bcd_list:
            bc_boolean_data_to_samples_md5[element] = True
        else:
            bc_boolean_data_to_samples_md5[element] = False
    # [print(bc) for bc in bc_boolean_data_to_samples_md5.items()]

    samples_to_data_check_md5 = True
    for key in bc_boolean_samples_to_data_md5:
        if not bc_boolean_samples_to_data_md5[key]:
            samples_to_data_check_md5 = False
            print("Sample {} lacks md5 data files.".format(key))

    data_to_samples_check_md5 = True
    for key in bc_boolean_data_to_samples_md5:
        if not bc_boolean_data_to_samples_md5[key]:
            data_to_samples_check_md5 = False
            print("md5 file {} refer to no sample".format(key))

    print("All samples have md5 data: {}. No unrelated md5 files remain on the hard drive: {}.".format(
        samples_to_data_check_md5,
        data_to_samples_check_md5))

    bc_boolean_samples_to_data_gz = {}
    for element in bcd_list:
        if element in filtered_bcs_gz_f:
            bc_boolean_samples_to_data_gz[element] = True
        else:
            bc_boolean_samples_to_data_gz[element] = False
    # [print(pair) for pair in bc_boolean_samples_to_data_gz.items()]

    bc_boolean_data_to_samples_gz = {}
    for element in filtered_bcs_gz_f:
        if element in bcd_list:
            bc_boolean_data_to_samples_gz[element] = True
        else:
            bc_boolean_data_to_samples_gz[element] = False
    # [print(bc) for bc in bc_boolean_data_to_samples_gz.items()]

    samples_to_data_check_gz = True
    for key in bc_boolean_samples_to_data_gz:
        if not bc_boolean_samples_to_data_gz[key]:
            samples_to_data_check_gz = False
            print("Sample {} lacks gz data files.".format(key))

    data_to_samples_check_gz = True
    for key in bc_boolean_data_to_samples_gz:
        if not bc_boolean_data_to_samples_gz[key]:
            data_to_samples_check_gz = False
            print("gz files {} refer to no sample".format(key))

    print("All samples have gz data: {}. No unrelated gz files remain on the hard drive: {}.".format(
        samples_to_data_check_gz,
        data_to_samples_check_gz))


folder_path = folder_path_request()
md5_list, md5_count = md5_searcher(folder_path)
gz_list, gz_count = gz_searcher(folder_path)
filtered_bcs_md5, filtered_bcs_gz = bc_filter(md5_list, gz_list)
bc_list = bc_list_generator("C:\\Users\\omega\\Desktop\\Barcode_list_for_data_checkup")
data_check(bc_list, filtered_bcs_md5, filtered_bcs_gz)
