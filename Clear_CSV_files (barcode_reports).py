import os


def clear_csv(directory_path, name = '.csv'):
    os.chdir(directory_path)
    list_of_files = os.listdir(os.getcwd())
    list_of_csv_local = []
    for n in list_of_files:
        if name in n:
            list_of_csv_local.append(n)
    for file in list_of_csv_local:
        os.remove(file)
# The function is used to clear all files that contain .csv in their name from the specified directory.


clear_csv('')
