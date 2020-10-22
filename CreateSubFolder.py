import os
from testcase_wndw import name_of_testcase
from tkinter import simpledialog
from tkinter import messagebox


def add_env():
    response = messagebox.askquestion("Info", "Do you have some environment")
    print(os.getcwd(), "In add env")
    folder_in_app = os.listdir()
    try:
        if response == 'yes':
            env_question = simpledialog.askstring("Environment!", "Enter Environment")
            try:
                if env_question not in folder_in_app:
                    os.mkdir(env_question)
                    os.chdir(os.path.join(os.getcwd(), env_question))
                    simpledialog.messagebox.showinfo("Exist!", 'Environment {} Folder Created'.format(env_question))
                    print("created in add", os.getcwd())
                elif env_question in folder_in_app:
                    os.chdir(os.path.join(os.getcwd(), env_question))
                    simpledialog.messagebox.showinfo("Exist!", 'Environment {} Folder Exist'.format(env_question))
                    print("Exist in add", os.getcwd())
            except:
                simpledialog.messagebox.showinfo("Exist!", 'Environment Folder Already Exist')
                os.chdir(os.path.join(os.getcwd(), env_question))
                print(os.getcwd(), "Exception from add env")
        elif response == 'no':
            os.mkdir("General")
            os.chdir(os.path.join(os.getcwd(), "General"))
            print("created", os.getcwd())
    except:
        simpledialog.messagebox.showinfo("Exist!", 'Environment Folder Already Exist')
        os.chdir(os.path.join(os.getcwd(), "General"))
        print(os.getcwd(), "Exception from add env")


def create_sub_folder(application_name):
    add_env()
    print(os.getcwd(), "Create Sub folder")
    # Take File Name from user
    print(application_name, "Application name")
    # If folder is not there create it
    list_of_files_in_folder = list()
    # Get list of all folders from the directory
    folders_in_scrnshot = os.listdir()
    for x in folders_in_scrnshot:
        list_of_files_in_folder.append(x)
    print(list_of_files_in_folder)
    try:
        if application_name not in list_of_files_in_folder:
            os.makedirs(application_name + "/Hands-on")
            # change directory path to screenshot/application name/hands-onn and passing it as param in Tracker
            os.chdir(os.path.join(os.getcwd(), application_name + "/Hands-on"))
            changing_dir = os.getcwd()
            print("Created", changing_dir)
            name_of_testcase()

        # If folder is already there the ask user to enter application name
        elif application_name in list_of_files_in_folder:
            # change directory path to screenshot/application name/hands-onn and passing it as param in Tracker
            os.chdir(os.path.join(os.getcwd(), application_name + "/Hands-on"))
            changing_dir = os.getcwd()
            print("Exist ", changing_dir)
            simpledialog.messagebox.showinfo("Exist!", 'Application {} Folder Already Exist'.format(application_name))
            name_of_testcase()
    # If user tries to enter something in lower an upper case both and that same file exist it will throw an exception
    # to handel that exception
    except:
        simpledialog.messagebox.showinfo("Exist!", 'Application {} Folder Already Exist'.format(application_name))
        os.chdir(os.path.join(os.getcwd(), application_name + "/Hands-on"))
        print(os.getcwd(), "Exception")
        name_of_testcase()
