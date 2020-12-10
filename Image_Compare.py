########################################################################################################################
# Author : Utkarsh Singh
# Project : Daily Utility
# Module : Compare And Get difference of two images from two different folder stored in 'Compare' folder inside Image
#          folder of the first Folder and also we can compare two individual files and storing with first file name with
#          just appended as "Compare" and "data"
########################################################################################################################
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import cv2
import os
import numpy as np
from pathlib import Path
import Utility_Launch


def img_c():
    img_cmpr = image_compare()


class image_compare(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("850x390+790+120")
        self.title("Image Comparison")
        self.resizable(False, False)
        self.focus_force()

        # Frame to hold top image
        self.first_frame = Frame(self, height=130, bg="white")
        self.first_frame.pack(fill='both')
        try:
            self.image_on_scrnshot = PhotoImage(file=os.path.join(Utility_Launch.path, 'Image_01/file.png'))
            self.label_photo = ttk.Label(self.first_frame, image=self.image_on_scrnshot,
                                         background="white").place(x=50, y=30)
        except:
            pass
        self.label_top_heading = ttk.Label(self.first_frame, text="Compare your JPG's and PNG's",
                                           font=("Times New Roman", 15)
                                           , background="white").place(x=190, y=40)

        # Two different tabs one for comparision through different folders and second for Single File Comparision
        self.tabcontrol = ttk.Notebook(self)
        self.tab1 = Frame(self.tabcontrol, bg="#4c6175", height=500)
        self.tab1.pack(fill="both")
        self.tab2 = Frame(self.tabcontrol, bg="#d9c284", height=500)
        self.tab2.pack(fill="both")

        # On File one for Folder by Folder Compare
        self.btn_im1 = ttk.Button(self.tab1, text="Folder 1", command=self.open_folder)
        self.btn_im1.place(x=700, y=70)
        self.btn_im2 = ttk.Button(self.tab1, text="Folder 2")
        self.btn_im2.place(x=700, y=150)

        # On Tab 2 for Single File Compare
        self.btn_img1 = ttk.Button(self.tab2, text="File 1", command=lambda: self.open_file())
        self.btn_img1.place(x=700, y=70)

        self.btn_img2 = ttk.Button(self.tab2, text="File 2")
        self.btn_img2.place(x=700, y=150)

        self.foldername = ttk.Entry(self.tab1, width=80)
        self.foldername.place(x=10, y=70)

        self.scndfoldername = ttk.Entry(self.tab1, width=80)
        self.scndfoldername.place(x=10, y=150)

        self.filename = ttk.Entry(self.tab2, width=80)
        self.filename.place(x=10, y=70)

        self.scndfilename = ttk.Entry(self.tab2, width=80)
        self.scndfilename.place(x=10, y=150)

        self.tabcontrol.add(self.tab1, text="Folder to Folder")
        self.tabcontrol.add(self.tab2, text="Image to Image")
        self.tabcontrol.pack(fill='both')
        self.btn_cmpr = ttk.Button(self.tab2, text="Compare")
        self.btn_cmpr.place(x=350, y=190)
        self.btn_cmpr2 = ttk.Button(self.tab1, text="Compare")
        self.btn_cmpr2.place(x=350, y=190)

    # Function to read and compare individual files
    def open_file(self):
        try:
            # First File Location
            self.filename['state'] = NORMAL
            self.filename.delete(0, END)
            filename = filedialog.askopenfilename(
                initialdir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Screenshot'),
                filetype=((".png files", "*.png"), (".jpg files", "*.jpg")),
                title='Open A File'
            )
            self.filename.insert(END, filename)
            self.filename['state'] = DISABLED

            # Second File Location
            def scn_file():
                self.scndfilename['state'] = NORMAL
                self.scndfilename.delete(0, END)
                scndfilename = filedialog.askopenfilename(
                    initialdir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Screenshot'),
                    filetype=((".png files", "*.png"), (".jpg files", "*.jpg")),
                    title='Open A File'
                )
                self.scndfilename.insert(END, scndfilename)
                self.scndfilename['state'] = DISABLED
                self.btn_cmpr.config(command=lambda: compare_img(filename, scndfilename))

            # Compare the two files
            def compare_img(f, f1):
                try:
                    path0 = f.replace(os.sep, '/')
                    path2 = f1.replace(os.sep, '/')
                    image1 = cv2.imread(path0)
                    image2 = cv2.imread(path2)
                    # compute difference
                    difference = cv2.subtract(image1, image2)
                    result = not np.any(difference)
                    if result is False:
                        # color the mask red
                        Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
                        ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
                        difference[mask != 255] = [0, 170, 255]

                        # add the red mask to the images to make the differences obvious
                        image2[mask != 255] = [0, 0, 255]
                        image1[mask != 255] = [0, 0, 255]
                        str(path0)
                        r = path0.split('.png')
                        t = r[0]
                        z = t + "compare.png"
                        q = t + "data.png"
                        y = os.path.join(path0, z)
                        x = os.path.join(path0, q)
                        cv2.imwrite(y, image1)
                        cv2.imwrite(x, difference)
                        messagebox.showinfo("Completed", "Difference occurred and the result images are stored "
                                                         "at {}".format(z))
                        self.destroy()
                        img_c()
                    else:
                        messagebox.showinfo("Completed", "No difference Occur")
                        self.filename['state'] = NORMAL
                        self.filename.delete(0, END)
                        self.scndfilename['state'] = NORMAL
                        self.scndfilename.delete(0, END)
                except:
                    messagebox.showerror("Wrong files maybe",
                                         "Please select correct files or the image files of same Size")
                    self.filename['state'] = NORMAL
                    self.filename.delete(0, END)
                    self.scndfilename['state'] = NORMAL
                    self.scndfilename.delete(0, END)

            self.btn_img2.config(command=scn_file)
        except:
            messagebox.showerror("Something went wrong", "Please select correct files or the image files of same Size")
            self.destroy()
            img_c()

    # Compare list of images from two separate folders
    def open_folder(self):
        try:
            # First Folder Location
            self.foldername['state'] = NORMAL
            self.foldername.delete(0, END)
            first_fldr = filedialog.askdirectory(
                initialdir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Screenshot'),
                title='Open A File'
            )
            self.foldername.insert(END, first_fldr)

            self.foldername['state'] = DISABLED

            # Second Folder location
            def scnd_fldr():
                self.scndfoldername['state'] = NORMAL
                self.scndfoldername.delete(0, END)
                scnd_folder = filedialog.askdirectory(
                    initialdir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Screenshot'),
                    title='Open A File'
                )
                self.scndfoldername.insert(END, scnd_folder)
                self.scndfoldername['state'] = DISABLED
                self.btn_cmpr2.config(command=lambda: self.compare_img(first_fldr, scnd_folder))

            self.btn_im2.config(command=scnd_fldr)
        except Exception as e:
            messagebox.showerror("Folder Issue", "Something went Wrong '{}'".format(e))
            self.destroy()
            img_c()

    # Compare image files from both the folders
    def compare_img(self, f, f2):
        try:
            path = Path(f)
            print(path)
            os.chdir(path)
            file = os.listdir()
            path2 = Path(f2)
            os.chdir(path2)
            file1 = os.listdir()
            last_file = file[-1]
            list_diff = list()
            if "Compare Result" not in file1:
                os.makedirs("Compare Result/Data")
            else:
                pass
            for i, j in zip(file, file1):
                if i.endswith('.png') or i.endswith('.JPG') and j.endswith('.png') or j.endswith('.JPG'):
                    print(i,"---",j)
                    image1 = cv2.imread(os.path.join(f, i))
                    image2 = cv2.imread(os.path.join(f2, j))
                    # compute difference
                    difference = cv2.subtract(image1, image2)
                    result = not np.any(difference)
                    if result is False:
                        list_diff.append(i)
                        # color the mask red
                        Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
                        ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
                        difference[mask != 255] = [0, 170, 255]

                        # add the red mask to the images to make the differences obvious
                        image1[mask != 255] = [0, 0, 255]
                        str(i)
                        img_name = i.split('.png')
                        o_img_name = img_name[0]
                        z = o_img_name + ".png"
                        q = o_img_name + "a.png"
                        save_loc = os.path.join(os.getcwd(),"Compare Result")
                        data_loc = os.path.join(save_loc,"Data")
                        y = os.path.join(save_loc, z)
                        x = os.path.join(data_loc, q)
                        cv2.imwrite(y, image1)
                        cv2.imwrite(x, difference)
                        if i == last_file:
                            messagebox.showinfo("Completed", "File is stored at {}/Compare Result".format(f2))
                            self.destroy()
                            img_c()
                        continue
                    else:
                        if i == last_file and len(list_diff) != 0:
                            messagebox.showinfo("Completed", "File is stored at {}/Compare Result".format(f2))
                            self.destroy()
                            img_c()
                        elif i == last_file and len(list_diff) == 0:
                            messagebox.showinfo("Completed", "No difference occurred")
                            self.destroy()
                            img_c()
                        continue
                else:
                    messagebox.showerror(".PNG or .JPG Files only","Please make sure your folder contains '.png' and"
                                                                   " '.jpg' files only ")
                    self.foldername['state'] = NORMAL
                    self.foldername.delete(0, END)
                    self.scndfoldername['state'] = NORMAL
                    self.scndfoldername.delete(0, END)
                    break
        except Exception as e:
            messagebox.showerror("Something went Wrong","Please check : {},'Remove folder if it exist in the "
                                                        "Compare Folder'".format(e))
            self.destroy()
            img_c()

