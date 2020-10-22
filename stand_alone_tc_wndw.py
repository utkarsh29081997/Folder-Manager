#########################################################################################################
# Author : Utkarsh Singh
# Project : Daily Utility
# Module : Window to create Test Case folder Called from main window and Continue flow for previous Flow
########################################################################################################
import os
from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter import ttk

from CheckDirectory import check_directory
from scrnshot_wndw import scrnshot
from testcase_wndw import name_of_testcase


# If the Application Folder already exist we do not need to call Create Folder part we can directly create Test case
class tc_window(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("550x550+700+120")
        self.title("One Stop Window")
        self.resizable(False, False)
        # Top Frame for icon and name
        self.frame_on_standalone = Frame(self, height=120, bg="white")
        self.frame_on_standalone.pack(fill="both")
        self.top_framestand_alone = PhotoImage(file='S:/Projects/Python Projects/Utility/Image_01/boy.png')
        self.label_photo = ttk.Label(self.frame_on_standalone, image=self.top_framestand_alone,
                                     background="white").place(x=30, y=30)
        self.label_heading = ttk.Label(self.frame_on_standalone, text="Get Done!!!", font=("Times New Roman", 15)
                                       , background="white").place(x=190, y=40)

        # Take Application name from drop down
        self.frame = Frame(self, height=530, bg='#c99a0c').pack(fill='both')
        self.get_app_list_from_env()
        print(os.getcwd(), "Here In standalone")
        self.get_app_name = StringVar(self)
        list_of_env = os.listdir()
        self.drp_dowlist_env = ttk.Combobox(self, width=27, textvariable=self.get_app_name, height=15, state="readonly")
        self.drp_dowlist_env['values'] = list_of_env
        self.drp_dowlist_env.place(x=50, y=130)
        self.drp_dowlist_env.set('Choose a File')
        self.create_btn1 = ttk.Button(self, width=14, text='      OK      ', command=self.app_name_for_testcase)
        self.create_btn1.place(x=50, y=184)
        self.pick_last = ttk.Button(self, width=14, text='Pick Last Flow', command=self.call_lastpick)
        self.pick_last.place(x=50, y=284)
        self.quit_app = ttk.Button(self, width=15, text='    Close    ', command=self.close_wndw)
        self.quit_app.place(x=175, y=184)

    def close_wndw(self):
        self.destroy()

    # Get Env. name and check in folder weather it exists or not in order to fetch the List of Application list
    def get_app_list_from_env(self):
        check_directory()
        response = messagebox.askquestion("!nfo", "Choose YES for a specific Environment and NO to move in General")
        print(os.getcwd())
        # Folders which are inside Screenshot
        folder_in_app = os.listdir()
        if response == 'yes':
            print(os.getcwd(), "get app env")
            env_question = simpledialog.askstring("Environment!", "Enter Environment (Case Sensitive)")
            if env_question in folder_in_app:
                os.chdir(os.path.join(os.getcwd(), env_question))
                simpledialog.messagebox.showinfo("Info!", 'Inside {} Environment Folder'.format(env_question))
            elif env_question not in folder_in_app:
                simpledialog.messagebox.showinfo("Error!", '{}Environment Folder does not exist'.format(env_question))
                self.get_app_list_from_env()
        elif response == 'no':
            os.chdir(os.path.join(os.getcwd(), "General"))
            print("created", os.getcwd())

    # Get application folder from Environment list
    def app_name_for_testcase(self):
        # Change the directory Since it will create the folder in Project File and we donn't need that so changing the
        # folder location to desktop screenshot
        print(self.get_app_name.get())
        if self.get_app_name.get() != "Choose a File":
            print(os.getcwd(), "In Sample 1")
            os.chdir(os.path.join(os.getcwd(), self.get_app_name.get() + "/Hands-on"))
            print(os.getcwd(), "In Sample 2")
            name_of_testcase()
            self.close_wndw()
        else:
            messagebox.showerror("Error!", "Please Enter Application name", icon="error")
            self.close_wndw()
            return tc_window()

    # To recreate last flow
    def call_lastpick(self):
        self.create_btn1['state'] = DISABLED
        print(os.getcwd(), "Before")
        # Take App name
        print(self.get_app_name.get())
        try:
            if self.get_app_name.get() != "Choose a File":
                print(os.getcwd(), "In Sample 1")
                app_foldr_name = self.get_app_name.get()
                os.chdir(os.path.join(os.getcwd(), app_foldr_name) + "/Hands-On")
                print(os.getcwd(), "In Sample 2")

                # Take test case name from the list
                get_tc = StringVar(self)
                list_of_files = os.listdir()
                drop_dwn_tc = ttk.Combobox(self, textvariable=get_tc, height=7, width=27, state="readonly")
                drop_dwn_tc.setvar("Choose TestCase File")
                drop_dwn_tc.place(x=50, y=320)
                drop_dwn_tc.set("Choose a Test Case")
                drop_dwn_tc['values'] = list_of_files

                start_btn1 = ttk.Button(self, width=14, text='      Start      '
                                        , command=lambda: self.call_scrnshot_for_lastpick(get_tc.get()))
                start_btn1.place(x=50, y=360)

            else:
                messagebox.showerror("Error!", "Please Select Application")
                self.close_wndw()
                return tc_window()
        except:
            messagebox.showerror("Error!", "Please Select Test Case")

    def call_scrnshot_for_lastpick(self, test_case_folder):
        if test_case_folder != "Choose a Test Case":
            self.close_wndw()
            print(test_case_folder, os.getcwd())
            test = test_case_folder
            os.chdir(os.path.join(os.getcwd(), test))
            print(os.getcwd(), "Here")
            scrnshot()
        else:
            messagebox.showerror("Error!", "Please Select Test Case")
