import os
import CreateFolder


# Getting or Changing Directory
def check_directory():
    # Getting Path current Folder and changing it to desktop if it's  not
    current_dir = os.getcwd()
    list_first = current_dir.split("/")

    # Find weather we are in Desktop folder or not
    if "Desktop" not in list_first:
        os.chdir("C:/Users/user/Desktop")
        change_directory = os.getcwd()
        print(change_directory)
        CreateFolder.create_folder()
    else:
        CreateFolder.create_folder()


