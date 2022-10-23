###############################################################
# Author : Utkarsh Singh
# Project : Daily Utility
# Module : Window to Enter Test Case Name
# Last Modified Date : 28 Dec,2020
###############################################################
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from test_case_track import track_test
import MCPI
import os


# The Third window where we need to Enter the Folder name of the application what I have done here is binded the button
# with the method and inside that method I have made a call to test_case_track and the rest of code is there
class name_of_testcase(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("450x450+120+120")
        self.title("Test Case")
        self.resizable(False, False)

        #  Top Frame to hold i and Label name
        self.frame_test = Frame(self, height=120, bg="white")
        self.frame_test.pack(fill="both")
        try:
            self.test_scren = PhotoImage(file=os.path.join(MCPI.path, 'Images/test.png'))
            self.test_photo = ttk.Label(self.frame_test, image=self.test_scren, background="white").place(x=50, y=30)
        except:
            pass
        self.heading = ttk.Label(self.frame_test, text="Test Case!!", font=("Times New Roman", 15),
                                 background="white")
        self.heading.place(x=190, y=40)

        # Bottom Frame to hold Test Case entry input and buttons
        self.frame = Frame(self, height=500, bg='#c99a0c').pack(fill='both')
        self.lbl = ttk.Label(self, text="Enter Test Case Name ", background='#c99a0c',
                             font=("Helvetica", 12)).place(x=61, y=180)
        self.enter_test_name = ttk.Entry(self, width=30)
        self.enter_test_name.place(x=60, y=215)
        self.enter_test_name.focus_force()
        self.create_btn = ttk.Button(self, width=14, text='      OK      ', command=lambda: self.create_test_name(None))
        self.create_btn.bind("<Return>", self.create_test_name)
        self.create_btn.place(x=60, y=250)
        self.quit_app = ttk.Button(self, width=15, text='    Close    ', command=lambda: self.close_wndw(None))
        self.quit_app.bind("<Return>", self.close_wndw)
        self.quit_app.place(x=185, y=250)

    def close_wndw(self, event):
        self.destroy()

    def create_test_name(self, event):
        test_name = self.enter_test_name.get()
        curr_dir = os.getcwd().split("\\")
        if 'Images' not in curr_dir:
            if test_name != '':
                track_test(test_name)
                self.close_wndw(None)
            else:
                messagebox.showerror("Error!", "Please Enter Test Case name")
                return name_of_testcase()
        elif 'Images' in curr_dir:
            messagebox.showerror("Not Allowed", "Please complete the previous Flow")
            self.close_wndw(None)
