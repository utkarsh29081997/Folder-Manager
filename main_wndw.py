################################################################
# Author : Utkarsh Singh
# Project : Daily Utility
# Module :  Main Window / Top Window
###############################################################
from tkinter import *
import app_wndw
from stand_alone_tc_wndw import tc_window
from tkinter import ttk
import os
import Excel_utility


def main():
    root = Tk()
    root.geometry("600x600+120+120")
    root.title("My Daily Utility App")
    root.resizable(False, False)
    frst = first_frame(root)
    root.mainloop()


def create_tc_wndw(event):
    Tc = tc_window()


def create_app_wndw(event):
    App = app_wndw.app_window()


def excel_util(event):
    exc = Excel_utility.excel_util()


# First Root file to call other class
# I have used ttk and tk components within this class to makes sure the design looks good and bindded the buttons
# with the two functions created outside the class
path = os.getcwd()


class first_frame(object):
    def __init__(self, master):
        self.master = master

        #  Top Frame to hold i and Label name
        self.icon_frame = Frame(master, height=120, bg="white").pack(fill="both")
        self.image = PhotoImage(file=os.path.join(path, 'Images/icon.png'))
        self.label_photo = ttk.Label(self.icon_frame, image=self.image, background="white").place(x=30, y=30)
        self.label_heading = ttk.Label(self.icon_frame, text="Daily Use", font=("Times New Roman", 15)
                                       , background="white").place(x=190, y=40)
        self.label_sub_head = ttk.Label(self.icon_frame, text="use to ease work.", font=("Times New Roman", 10),
                                        background="white").place(x=190, y=80)

        # Bottom Frame to hold  buttons
        self.frame_bottom = Frame(master, height=500, bg='#575653')
        self.frame_bottom.pack(fill='both')
        self.create_btn = ttk.Button(self.frame_bottom, text='Create Application Folder ',
                                     command=lambda: create_app_wndw(None))
        self.create_btn.bind("<Return>", create_app_wndw)
        self.create_btn.place(x=50, y=100)
        self.create_test_case = ttk.Button(self.frame_bottom, text='Create Test Case Folder     ',
                                           command=lambda:create_tc_wndw(None))
        self.create_test_case.bind("<Return>", create_tc_wndw)
        self.create_test_case.place(x=50, y=170)
        self.work_excel = ttk.Button(self.frame_bottom, text='Work with Excel        ',
                                           command=lambda:excel_util(None))
        self.work_excel.bind("<Return>",excel_util)
        self.work_excel.place(x=50, y=240)


if __name__ == '__main__':
    main()
