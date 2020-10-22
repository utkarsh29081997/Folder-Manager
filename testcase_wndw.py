################################################################
# Author : Utkarsh Singh
# Project : Daily Utility
# Module : Window to Enter Test Case Name
###############################################################
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from test_case_track import track_test


# The Third window where we need to Enter the Folder name of the application what I have done here is binded the button
# with the method and inside that method I have made a call to test_case_track and the rest of code is there
class name_of_testcase(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("450x450+120+120")
        self.title("Test Case")
        self.resizable(False, False)

        #  Top Frame to hold Image and Label name
        self.top_test = Frame(self, height=120, bg="white")
        self.top_test.pack(fill="both")
        self.image_on_test = PhotoImage(file='S:/Projects/Python Projects/Utility/Image/test.png')
        self.label_top_heading = ttk.Label(self.top_test, text="Test Case", font=("Times New Roman", 15)
                                           , background="white")
        self.label_photo = ttk.Label(self.top_test, image=self.image_on_test, background="white")
        self.label_photo.place(x=50, y=30)
        self.label_top_heading.place(x=190, y=40)

        # Bottom Frame to hold Test Case entry input and buttons
        self.frame = Frame(self, height=500, bg='#c99a0c').pack(fill='both')
        self.lbl = ttk.Label(self, text="Enter Test Case Name ", background='#c99a0c',
                             font=("Helvetica", 12)).place(x=61, y=180)
        self.enter_test_name = ttk.Entry(self, width=30)
        self.enter_test_name.place(x=60, y=215)
        self.enter_test_name.focus_force()
        self.create_btn = ttk.Button(self, width=14, text='      OK      ', command=self.create_test_name)
        self.create_btn.place(x=60, y=250)
        self.quit_app = ttk.Button(self, width=15, text='    Close    ', command=self.close_wndw)
        self.quit_app.place(x=185, y=250)

    def close_wndw(self):
        self.destroy()

    def create_test_name(self):
        test_name = self.enter_test_name.get()
        if test_name != '':
            track_test(test_name)
            self.close_wndw()
        else:
            messagebox.showerror("Error!", "Please Enter Test Case name", icon="error")
            return name_of_testcase()
