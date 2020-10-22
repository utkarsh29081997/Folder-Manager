#######################################################################
# Author : Utkarsh Singh
# Project : Daily Utility
# Module : Window to take Screenshot and Enter images into the word
######################################################################
import datetime
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import pyscreenshot
from docx import Document
from docx.shared import Cm


def get_file_dir():
    current_dir = os.getcwd()
    list_first = list()
    print(os.getcwd())
    list_first = current_dir.split("/")
    if "Images" not in list_first:
        os.chdir(os.path.join(os.getcwd(), 'Images'))
    print(os.getcwd(), "In fil_dir")


# The main part of the story is here there are two functions created outside the class as if created inside the class
# It would have lost it's path as once the function is called it would have binded itself with /Images once again which
# never exists so need to create it as function instead of method and since we only want it to bind itself with the
# /Images once we need to load it only  once so I had found this solution

class scrnshot(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        get_file_dir()
        print(os.getcwd(), "Here in screen shot")
        self.geometry("350x350+120+120")
        self.title("Take Screenshot")
        self.resizable(False, False)

        # Top frame to hold image and Name
        self.top_scrnshot = Frame(self, height=120, bg="white")
        self.top_scrnshot.pack(fill="both")
        self.image_on_scrnshot = PhotoImage(file='S:/Projects/Python Projects/Utility/Image_01/smartphone.png')
        self.label_top_heading = ttk.Label(self.top_scrnshot, text="Snap It.", font=("Times New Roman", 15)
                                           , background="white").place(x=190, y=40)
        self.label_heading = ttk.Label(self.top_scrnshot, text="Save It!!!", font=("Times New Roman", 10)
                                       , background="white").place(x=190, y=80)
        self.label_photo = ttk.Label(self.top_scrnshot, image=self.image_on_scrnshot, background="white")
        self.label_photo.place(x=50, y=30)

        # Bottom frame to hold buttons
        self.frame = Frame(self, height=300, bg='#c99a0c').pack(fill='both')
        self.take_scrn = ttk.Button(self, text='    Take ScreenShot    ', command=self.save_img)
        self.take_scrn.place(x=60, y=150)
        self.save_to_wrd = ttk.Button(self, width=15, text='    Save To word   ', command=self.defect_or_not)
        self.save_to_wrd.place(x=60, y=210)

    def save_img(self):
        self.withdraw()
        image = pyscreenshot.grab()
        current = str(datetime.datetime.now())
        date, times = current.split()
        hour, minutes, seconds = times.split(":")
        file = hour + "_" + minutes + "_" + seconds
        image.save(file + ".png")
        self.update()
        self.deiconify()

    def close_wndw(self):
        self.destroy()

    def write_in_file(self):
        old_dir = os.getcwd()
        list_of_files_images = os.listdir()
        current_dir = old_dir.rstrip("/Images")
        os.chdir(current_dir)
        print(os.getcwd())
        listt = list()
        doc = Document()
        for x in list_of_files_images:
            y = os.path.join(old_dir, x)
            listt.append(y)
            print(listt)
        for x in listt:
            doc.add_picture(x, width=Cm(10))
        name = current_dir.split()
        print(name)
        *_, doc_name = name
        doc_name = doc_name.rstrip(r"\\")
        print(doc_name, "DOC Name")
        doc.save(doc_name + ".docx")
        print("In read mode")
        messagebox.showinfo("Done!", "Your folder is saved with name {}".format(doc_name))
        self.close_wndw()

    def defect_or_not(self):
        user_res = messagebox.askquestion("Info!!", "Was it a defect")
        if user_res == 'no':
            self.write_in_file()
