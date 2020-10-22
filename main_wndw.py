################################################################
# Author : Utkarsh Singh
# Project : Daily Utility
# Module :  Main Window / Top Window
###############################################################
from tkinter import *
import app_wndw
from stand_alone_tc_wndw import tc_window
from tkinter import ttk


def main():
    root = Tk()
    root.geometry("600x600+120+120")
    root.title("Utility")
    root.resizable(False, False)
    frst = first_frame(root)
    root.mainloop()


def create_tc_wndw():
    Tc = tc_window()


def create_app_wndw():
    App = app_wndw.app_window()


# First Root file to call other class
# I have used ttk and tk components within this class to makes sure the design looks good and bindded the buttons
# with the two functions created outside the class

class first_frame(object):
    def __init__(self, master):
        self.master = master

        #  Top Frame to hold Image and Label name
        self.icon_frame = Frame(master, height=120, bg="white").pack(fill="both")
        self.image = PhotoImage(file='S:/Projects/Python Projects/Utility/Images/icon.png')
        self.label_photo = ttk.Label(self.icon_frame, image=self.image, background="white").place(x=30, y=30)
        self.label_heading = ttk.Label(self.icon_frame, text="Daily Use", font=("Times New Roman", 15)
                                       , background="white") .place(x=190, y=40)
        self.label_sub_head = ttk.Label(self.icon_frame, text="use to ease work.", font=("Times New Roman", 10),
                                        background="white").place(x=190, y=80)

        # Bottom Frame to hold  buttons
        self.frame_bottom = Frame(master, height=500, bg='#575653')
        self.frame_bottom.pack(fill='both')
        self.create_btn = ttk.Button(self.frame_bottom, text='Create Application Folder ',
                                     command=create_app_wndw)
        self.create_btn.place(x=50,y=100)
        self.create_test_case = ttk.Button(self.frame_bottom, text='Create Test Case Folder     ',
                                           command=create_tc_wndw)
        self.create_test_case.place(x=50,y=170)


if __name__ == '__main__':
    main()
