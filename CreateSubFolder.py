import os
from testcase_wndw import name_of_testcase
from tkinter import simpledialog
from tkinter import messagebox


def add_env():
    response = messagebox.askquestion("Just Asking", "Add in environment ? ")
    try:
        if response == 'yes':
            env_question = simpledialog.askstring("Environment!", "Enter Environment")
            check_env(env_question)
        elif response == 'no':
            os.mkdir("General")
            os.chdir(os.path.join(os.getcwd(), "General"))
    except:
        simpledialog.messagebox.showinfo("Exist!", 'Saving in General Folder')
        os.chdir(os.path.join(os.getcwd(), "General"))


def check_env(env_question_add):
    folder_in_app = os.listdir()
    env_question = env_question_add
    if env_question != '':
        try:
            if env_question not in folder_in_app:
                os.mkdir(env_question)
                os.chdir(os.path.join(os.getcwd(), env_question))
                simpledialog.messagebox.showinfo("Created!", 'Environment {} Folder Created'.format(env_question))
            elif env_question in folder_in_app:
                os.chdir(os.path.join(os.getcwd(), env_question))
                simpledialog.messagebox.showinfo("Exist!", 'Environment {} Folder Exist'.format(env_question))
        except:
            simpledialog.messagebox.showinfo("Exist!", 'Environment Folder Already Exist')
            os.chdir(os.path.join(os.getcwd(), env_question))
    else:
        messagebox.showerror("Error!", "Environment field cannot be blank")
        return add_env()


def create_sub_folder(application_name):
    add_env()
    # Take File Name from user
    # If folder is not there create it
    list_of_files_in_folder = list()
    # Get list of all folders from the directory
    folders_in_scrnshot = os.listdir()
    for x in folders_in_scrnshot:
        list_of_files_in_folder.append(x)
    try:
        if application_name not in list_of_files_in_folder:
            os.makedirs(application_name)
            # change directory path to screenshot/application name/hands-on and passing it as param in Tracker
            os.chdir(os.path.join(os.getcwd(), application_name))
            name_of_testcase()

        # If folder is already there the ask user to enter application name
        elif application_name in list_of_files_in_folder:
            # change directory path to screenshot/application name/hands-onn and passing it as param in Tracker
            os.chdir(os.path.join(os.getcwd(), application_name))
            simpledialog.messagebox.showinfo("Exist!", 'Application {} Folder Already Exist'.format(application_name))
            name_of_testcase()
    # If user tries to enter something in lower an upper case both and that same file exist it will throw an exception
    # to handel that exception
    except:
        simpledialog.messagebox.showinfo("Exist!", 'Application {} Folder Already Exist'.format(application_name))
        os.chdir(os.path.join(os.getcwd(), application_name))
        name_of_testcase()
