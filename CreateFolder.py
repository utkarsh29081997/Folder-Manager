import os


# Creating Folder Screenshot in Desktop
def create_folder():
    os.getcwd()
    # Check weather Screenshot folder is already created or not
    list_of_files = list()
    folders_on_desk = os.listdir()
    for x in folders_on_desk:
        file_name, file_extn = os.path.splitext(x)
        list_of_files.append(file_name)
    # If folder is not there create it
    if "Screenshot" not in list_of_files:
        os.mkdir("Screenshot")
        os.chdir("C:/Users/user/Desktop/Screenshot")
        print("Made")

    # If folder is already there the ask user to enter application name
    elif "Screenshot" in list_of_files:
        os.chdir("C:/Users/user/Desktop/Screenshot")
        print(os.getcwd())
        print("Exist from Create Folder")
