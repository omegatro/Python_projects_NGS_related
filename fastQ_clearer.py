import os
import re
import sys
import csv


def folder_path_request(bc_list_to_check):
    folder_path_to_check = input("Enter the path you want to check or type n to quit the script: ")
    folder_path_to_check = re.escape(folder_path_to_check)
    # Adjusts the windows format path to the python format path.
    if folder_path_to_check == "n":
        sys.exit("The script is closing.")
    #   Stops the script execution.
    elif not os.path.exists(folder_path_to_check):
        print("The path doesn't exist.")
        folder_path_request(barcode_list)
    #   Recursively invites the user to enter valid path.
    else:
        print("The folder path to clear is: " + folder_path_to_check)
        list_of_folders = [f.path for f in os.scandir(folder_path_to_check) if f.is_dir()]
        list_of_files = []
        [list_of_files.append(os.listdir(path)) for path in list_of_folders]
        # Scans for files in the folders to be deleted.
        print("The following files will be deleted: ")
        [print("    " + file_name_local) for file_name in list_of_files for file_name_local in file_name if
         file_name_local not in bc_list_to_check]
        user_confirm = input("Type y to confirm the folder path, or type anything else to reject the"
                             " folder path: ")
        if user_confirm == "y":
            print(folder_path_to_check)
            return folder_path_to_check
        else:
            print("The path was not confirmed.")
            folder_path_request(barcode_list)
        #    Recursively invites the user to enter valid path.


def file_deleter(path_folder_to_clear, barcode_list):
    list_of_folders = [f.path for f in os.scandir(path_folder_to_clear) if f.is_dir()]
    lists_of_file_names = []
    [lists_of_file_names.append(os.listdir(path)) for path in list_of_folders]
    # os.listdir() scans the folder and generates a list of file names in string format.
    file_count = 0
    deleted_files = []
    for path in list_of_folders:
        os.chdir(path)
        for f_names in lists_of_file_names:
            for file_name_value in f_names:
                if os.path.exists(file_name_value):
                    if file_name_value not in barcode_list:
                        deleted_files.append(file_name_value)
                        file_count += 1
                        os.remove(file_name_value)
    print(str(file_count) + " files were deleted in the specified folder.")
    if len(deleted_files) != 0:
        print("Here is the list of names for the files that were deleted: ")
        [print(deleted_file_name) for deleted_file_name in deleted_files]
        file_deleter(folder_path_request(barcode_list), barcode_list)
    else:
        print("The folder contained no files of any specified format to be deleted.")
        file_deleter(folder_path_request(barcode_list), barcode_list)


os.chdir("C:\\Users\\omega\\Desktop\\Barcode_list_for_data_checkup")
reader = csv.reader(open("Barcode_list_fastQ.csv", 'r'))
bc_list = []
for row in reader:
    bc_list.append(row[0])

bc_list_final = []
for name in bc_list:
    bc_list_final.append(name + "_1.fq.gz")
    bc_list_final.append(name + "_2.fq.gz")
    bc_list_final.append(name + "_1.fq.gz.md5")
    bc_list_final.append(name + "_2.fq.gz.md5")
# [print(name) for name in bc_list_final]

file_deleter(folder_path_request(bc_list_final), bc_list_final)
