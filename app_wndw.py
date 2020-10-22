################################################################
# Author : Utkarsh Singh
# Project : Daily Utility
# Module : Window to Enter Application Name
###############################################################
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import CreateSubFolder
from CheckDirectory import check_directory


# The second window where we need to Enter the Folder name of the application what I have done here is binded the button
# with the method and inside that method I have made a call to CreateSubFolder and the rest of code is there
class app_window(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("450x450+120+120")
        self.title("Application Name")
        self.resizable(False, False)

        #  Top Frame to hold Image and Label name
        self.top_frame = Frame(self, height=120, bg="white")
        self.top_frame.pack(fill="both")
        self.image_on_app = PhotoImage(file='S:/Projects/Python Projects/Utility/Images/folder.png')
        self.label_photo = ttk.Label(self.top_frame, image=self.image_on_app, background="white")
        self.label_photo.place(x=50, y=30)
        self.label_heading = ttk.Label(self.top_frame, text="Application", font=("Times New Roman", 15),
                                       background="white")
        self.label_heading.place(x=190, y=40)

        # Bottom Frame to hold Application entry input and buttons
        self.frame = Frame(self, height=500, bg='#c99a0c').pack(fill='both')
        self.lbl = ttk.Label(self, text="Enter Application Name ", background='#c99a0c',
                             font=("Helvetica", 12)).place(x=61, y=180)
        self.entry_name = ttk.Entry(self, width=30)
        self.entry_name.place(x=60, y=215)
        self.entry_name.focus_force()
        self.create_btn = ttk.Button(self, width=14, text='Create', command=self.create_sub_folder)
        self.create_btn.place(x=60, y=250)
        self.quit_app = ttk.Button(self, width=15, text='Close', command=self.close_wndw)
        self.quit_app.place(x=185, y=250)

    def close_wndw(self):
        self.destroy()

    def create_sub_folder(self):
        application_name = self.entry_name.get()
        if application_name != '':
            check_directory()
            CreateSubFolder.create_sub_folder(application_name)
            self.close_wndw()
        else:
            messagebox.showerror("Error!", "Please Enter Application name", icon="error")
            self.close_wndw()
            return app_window()
