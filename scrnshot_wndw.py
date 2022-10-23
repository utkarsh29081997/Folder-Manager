#######################################################################
# Author : Utkarsh Singh
# Project : Daily Utility
# Module : Window to take Screenshot and Enter images into the word
# Last Modified Date : 07 Mar,2020
######################################################################
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageGrab, Image
import time

import MCPI
from docx import Document
from docx.shared import Cm
from defect_file_crtn import defect_file
from Logging_files import log_in_excel


# def get_file_dir():
#     current_dir = os.getcwd()
#     if "Images" not in current_dir:
#         os.chdir(os.path.join(current_dir, 'Images'))  # Removed /Hands-on


# The main part of the story is here there are two functions created outside the class as if created inside the class
# It would have lost it's path as once the function is called it would have binded itself with /Images once again which
# never exists so need to create it as function instead of method and since we only want it to bind itself with the
# /Images once we need to load it only  once so I had found this solution
class scrnshot(Toplevel):
    def __init__(self,imagefldrpath):
        try:
            Toplevel.__init__(self)
            # get_file_dir()
            self.geometry("350x350+120+120")
            self.title("Take Screenshot")
            self.resizable(False, False)
            os.chdir(imagefldrpath)
            o_path = os.getcwd()
            # Top frame to hold image and Name
            self.frame_on_scrnshot = Frame(self, height=120, bg="white")
            self.frame_on_scrnshot.pack(fill="both")
            try:
                self.image_on_scrnshot = PhotoImage(file=os.path.join(MCPI.path, 'Image_01/sp.png'))
                self.label_photo = ttk.Label(self.frame_on_scrnshot, image=self.image_on_scrnshot,
                                             background="white").place(x=50, y=30)
            except:
                pass
            self.label_top_heading = ttk.Label(self.frame_on_scrnshot, text="Snap It.", font=("Times New Roman", 15)
                                               , background="white").place(x=190, y=40)
            self.label_heading_ss = ttk.Label(self.frame_on_scrnshot, text="Save It!!!", font=("Times New Roman", 10)
                                              , background="white").place(x=190, y=80)

            # Bottom frame to hold buttons
            self.frame = Frame(self, height=300, bg='#c99a0c').pack(fill='both')
            self.take_scrn = ttk.Button(self, text='    Take ScreenShot    ', command=lambda: self.save_img(None, o_path))
            self.take_scrn.bind("<Return>", self.save_img)
            self.take_scrn.place(x=60, y=150)
            self.save_to_wrd = ttk.Button(self, width=15, text='    Save To word   ',
                                          command=lambda: self.defect_or_not(None))
            self.save_to_wrd.bind("<Return>", self.defect_or_not)
            self.save_to_wrd.place(x=60, y=210)
        except:
            messagebox.showerror("Error", "Something went Wrong")
            self.close_wndw()

    def save_img(self, event, o_path):
        try:
            self.withdraw()
            time.sleep(2)
            image = ImageGrab.grab()
            # current = str(datetime.datetime.now())
            # date, times = current.split()
            # hour, minutes, seconds = times.split(":")
            # file = hour + "_" + minutes + "_" + seconds
            # file_name = file + ".png"
            if os.getcwd() == o_path:  # Line 75 and 76 makes sure that only one flow gets executed at a time i.e.
                list_of_img = os.listdir()  # Latest flow always
                if len(list_of_img) != 0:
                    f = list_of_img[-1]
                    if f.endswith('.png'):
                        name, ext = os.path.splitext(f)
                        c_name = name.split()
                        nmbr = c_name[-1]
                        nmbr = int(nmbr) + 1
                        nmbr = str(nmbr).zfill(4)
                        file_name = 'Screenshot ' + nmbr + ext
                        image.save(file_name)
                    else:
                        messagebox.showwarning("Warning!!",
                                               "Please remove the file which is not in .png format or rename "
                                               "it so that it does not appear in the end")
                else:
                    image.save('Screenshot 0000.png')
                self.update()
                self.deiconify()
            else:
                messagebox.showerror("Invalid Attempt", "Please Complete one flow at once")
                self.close_wndw()
        except:
            self.close_wndw()

    def close_wndw(self):
        self.destroy()

    def write_in_file(self):
        old_dir = os.getcwd()
        list_of_files_images = os.listdir()
        current_dir = old_dir.rstrip("/Images")
        os.chdir(current_dir)
        doc = Document()
        listt = [os.path.join(old_dir, x) for x in list_of_files_images if x.endswith('.png') or x.endswith('.JPG')]
        if len(listt) != 0:
            for x in listt:
                doc.add_picture(x, width=Cm(10))
            name = current_dir.split()
            *_, doc_name = name
            doc_name = doc_name.rstrip(r"\\")
            doc.save(doc_name + ".docx")
            messagebox.showinfo("Done!", "Your file is saved with name {}".format(doc_name))
            log_in_excel(os.getcwd(), 'Pass', ' ', ' ', ' ')
            self.close_wndw()
        else:
            messagebox.showerror("Error!", "Nothing to save")
            self.close_wndw()

    def defect_or_not(self, event):
        user_res = messagebox.askquestion("Info!!", "Was it a defect")
        if user_res == 'no':
            self.write_in_file()
        elif user_res == 'yes':
            self.close_wndw()
            defect_file()
