#########################################################################################################
# Author : Utkarsh Singh
# Project : Daily Utility
# Module : Window to create Test Case folder Called from main window and Continue flow for previous Flow
# Last Modified Date : 13 Dec,2020
########################################################################################################
import os
from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter import ttk
import MCPI

from CheckDirectory import check_directory
from scrnshot_wndw import scrnshot
from testcase_wndw import name_of_testcase


# If the Application Folder already exist we do not need to call Create Folder part we can directly create Test case
class tc_window(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("550x450+790+120")
        self.title("One Stop Window")
        self.resizable(False, False)

        # Top Frame for icon and name
        self.frame_on_standalone = Frame(self, height=120, bg="white")
        self.frame_on_standalone.pack(fill="both")
        try:
            self.top_framestand_alone = PhotoImage(file=os.path.join(MCPI.path, 'Image_01/boy.png'))
            self.label_photo = ttk.Label(self.frame_on_standalone, image=self.top_framestand_alone,
                                         background="white").place(x=30, y=30)
        except:
            pass
        self.label_heading = ttk.Label(self.frame_on_standalone, text="Get Done!!!", font=("Times New Roman", 15)
                                       , background="white").place(x=190, y=40)
        # If no Folder exists in Screenshot it will destroy the current window without any exception
        try:
            # Take Application name from drop down
            self.frame = Frame(self, height=530, bg='#c99a0c').pack(fill='both')
            self.get_app_list_from_env()
            self.focus()
            self.get_app_name = StringVar(self)
            list_of_env = os.listdir()
            self.drp_dowlist_env = ttk.Combobox(self,width=27,textvariable=self.get_app_name,height=15,state="readonly")
            self.drp_dowlist_env['values'] = list_of_env
            self.drp_dowlist_env.place(x=50, y=130)
            self.drp_dowlist_env.set('Choose a File')
            self.create_btn1 = ttk.Button(self, width=14, text='      OK      ',
                                          command=lambda:self.app_name_for_testcase(None))
            self.create_btn1.bind("<Return>",self.app_name_for_testcase)
            self.create_btn1.place(x=50, y=184)
            self.quit_app = ttk.Button(self, width=15, text='    Close    ', command=lambda: self.close_wndw(None))
            self.quit_app.bind("<Return>", self.close_wndw)
            self.quit_app.place(x=178, y=184)
            self.pick_last = ttk.Button(self, width=14, text='Pick Last Flow', command=lambda:self.call_lastpick(None))
            self.pick_last.bind("<Return>",self.call_lastpick)
            self.pick_last.place(x=50, y=284)

        except Exception as e:
            messagebox.showerror("Wait!!", e)
            pass

    def close_wndw(self,event):
        self.destroy()

    # Get Env. name and check in folder wea there it exists or not in order to fetch the List of Application list
    def get_app_list_from_env(self):
        check_directory()
        response = messagebox.askquestion("!nfo", "Choose YES for a specific Environment and NO to move in General")
        # Folders which are inside Screenshot
        folder_in_app = os.listdir()
        try:
            if response == 'yes':
                env_question = simpledialog.askstring("Environment!", "Enter Environment (Case Sensitive)")
                if env_question in folder_in_app:
                    os.chdir(os.path.join(os.getcwd(), env_question))
                    simpledialog.messagebox.showinfo("Info!", 'Inside {} Environment Folder'.format(env_question))
                elif env_question not in folder_in_app:
                    simpledialog.messagebox.showinfo("Error!",
                                                     '{} Environment Folder does not exist'.format(env_question))
                    self.get_app_list_from_env()
            elif response == 'no':
                os.chdir(os.path.join(os.getcwd(), "General"))
        except:
            simpledialog.messagebox.showinfo("Error!", 'No Folder available in Screenshot')
            self.close_wndw(None)

    # Get application folder from Environment list
    def app_name_for_testcase(self,event):
        # Change the directory Since it will create the folder in Project File and we donn't need that so changing the
        # folder location to desktop screenshot
        if self.get_app_name.get() != "Choose a File":
            os.chdir(os.path.join(os.getcwd(), self.get_app_name.get()))
            name_of_testcase()
            self.close_wndw(None)
        else:
            messagebox.showerror("Error!", "Please Enter Application name", icon="error")
            self.focus()

    # To recreate last flow
    def call_lastpick(self,event):
        # Take App name
        try:
            self.create_btn1['state'] = DISABLED
            self.pick_last['state'] = DISABLED
            if self.get_app_name.get() != "Choose a File":
                app_foldr_name = self.get_app_name.get()
                os.chdir(os.path.join(os.getcwd(), app_foldr_name))
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
                self.create_btn1['state'] = NORMAL
                self.pick_last['state'] = NORMAL
                self.focus()
        except:
            messagebox.showerror("Error!", "Please Select Test Case")
            self.focus()

    def call_scrnshot_for_lastpick(self, test_case_folder):
        if test_case_folder != "Choose a Test Case":
            self.close_wndw(None)
            test = test_case_folder
            os.chdir(os.path.join(os.getcwd(), test))
            imgfldrpath = os.path.join(os.getcwd(), 'Images')
            scrnshot(imgfldrpath)
        else:
            messagebox.showerror("Error!", "Please Select Test Case")
            self.focus()
