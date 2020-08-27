import os

folder_path_to_check = "C:\\Users\\omega\\PycharmProjects\\PythonLearn101\\Test_files\\Summary_reports"
file_list = os.listdir(folder_path_to_check)
print("There are the following .html files in the  Summary report folder: ")
[print("    " + f_name) for f_name in file_list if ".html" in f_name]
file_count = 0
deleted_files = []
user_confirm = input("Type y to confirm cleanup operation for Summary reports: ")
if user_confirm == "y":
    print("Cleanup confirmed.")
    for name in file_list:
        if os.path.exists(name):
            if ".html" in name:
                deleted_files.append(name)
                file_count += 1
                os.remove(name)
    print("The following " + str(file_count) + " files were deleted: ")
    [print("    " + name) for name in deleted_files]
else:
    print("The path was not confirmed.")
