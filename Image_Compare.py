########################################################################################################################
# Author : Utkarsh Singh
# Project : Daily Utility
# Module : Compare And Get difference of two images from two different folder stored in 'Compare' folder inside Image
#          folder of the first Folder and also we can compare two individual files and storing with first file name with
#          just appended as "Compare" and "data"
# Last Modified Date : 20 Dec,2020
########################################################################################################################
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import cv2
import os
import numpy as np
from pathlib import Path
import Utility_Launch
import datetime


def img_c():
    img_cmpr = image_compare()


class image_compare(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("780x390+790+120")
        self.title("Image Comparison")
        self.resizable(False, False)
        self.focus_force()

        # Frame to hold top image
        self.first_frame = Frame(self, height=130, bg="white")
        self.first_frame.pack(fill='both')
        try:
            self.image_on_imgcmpr = PhotoImage(file=os.path.join(Utility_Launch.path, 'Image_01/file.png'))
            self.label_photo = ttk.Label(self.first_frame, image=self.image_on_imgcmpr,
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
        self.btn_im1 = ttk.Button(self.tab1, text="Target Folder", command=self.open_folder)
        self.btn_im1.place(x=670, y=70)
        self.btn_im2 = ttk.Button(self.tab1, text="Source Folder")
        self.btn_im2.place(x=670, y=150)

        # On Tab 2 for Single File Compare
        self.btn_img1 = ttk.Button(self.tab2, text="Target File", command=self.open_file)
        self.btn_img1.place(x=670, y=70)

        self.btn_img2 = ttk.Button(self.tab2, text="Source File")
        self.btn_img2.place(x=670, y=150)

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
        self.btn_cmpr['state'] = DISABLED
        self.btn_cmpr2 = ttk.Button(self.tab1, text="Compare")
        self.btn_cmpr2.place(x=350, y=190)
        self.btn_cmpr2['state'] = DISABLED

    # Function to read individual image {.png and .jpg}files
    def open_file(self):
        try:
            # First File Location
            # Disabling the buttons once we get the locations of the file
            # Delete the Entry value i.e. location if one of the location remains empty and disable the compare button
            self.filename['state'] = NORMAL
            self.filename.delete(0, END)
            self.scndfilename['state'] = NORMAL
            self.scndfilename.delete(0, END)
            self.btn_cmpr['state'] = DISABLED
            filename = filedialog.askopenfilename(
                initialdir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Screenshot'),
                filetype=((".png files", "*.png"), (".jpg files", "*.jpg")),
                title='Open A File'
            )
            if filename:
                self.filename.insert(END, filename)
                self.filename['state'] = DISABLED

                # Second File Location
                def scn_file():
                    self.scndfilename['state'] = NORMAL
                    self.scndfilename.delete(0, END)
                    self.btn_cmpr['state'] = DISABLED
                    scndfilename = filedialog.askopenfilename(
                        initialdir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Screenshot'),
                        filetype=((".png files", "*.png"), (".jpg files", "*.jpg")),
                        title='Open A File'
                    )
                    if scndfilename:
                        self.scndfilename.insert(END, scndfilename)
                        self.scndfilename['state'] = DISABLED
                        self.btn_cmpr['state'] = NORMAL
                        self.btn_cmpr.config(command=lambda: compare_img(filename, scndfilename))
                    elif self.scndfilename.get() == '':
                        self.btn_cmpr['state'] = DISABLED
                        self.filename['state'] = NORMAL
                        self.filename.delete(0, END)
                        messagebox.showerror("Error", "Please Select Source File")

                self.btn_img2.config(command=scn_file)
            elif self.filename.get() == '':
                self.btn_cmpr['state'] = DISABLED
                messagebox.showerror("Error", "Please Select Target File")

            def compare_img(filename, scndfilename):
                self.filename['state'] = NORMAL
                compare_img_files(filename, scndfilename)
                self.filename.delete(0, END)
                self.scndfilename['state'] = NORMAL
                self.scndfilename.delete(0, END)
                self.destroy()
                img_c()

        except Exception as e:
            messagebox.showerror("Something went wrong", "Please Check {} \nPossible Reasons of Failure"
                                                         "\n1.The files would be created from different machines "
                                                         "or it could be taken from internet"
                                                         "\n2.Please select correct files or the image files of "
                                                         "same Size"
                                                         "\n3.If your reason is not mentioned contact developing "
                                                         "team".format(e))
            self.destroy()
            img_c()

    # Compare list of images from two separate folders
    def open_folder(self):
        try:
            # First Folder Location
            # Disabling the buttons once we get the locations of the file
            # Delete the Entry value i.e. location if one of the location remains empty and disable the compare button
            self.foldername['state'] = NORMAL
            self.foldername.delete(0, END)
            self.scndfoldername['state'] = NORMAL
            self.scndfoldername.delete(0, END)
            self.btn_cmpr2['state'] = DISABLED
            first_fldr = filedialog.askdirectory(
                initialdir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Screenshot'),
                title='Open A File'
            )
            self.foldername.insert(END, first_fldr)
            if first_fldr and self.foldername.get() != '':
                self.foldername['state'] = DISABLED

                # Second Folder location
                def scnd_fldr():
                    try:
                        self.scndfoldername['state'] = NORMAL
                        self.scndfoldername.delete(0, END)
                        self.btn_cmpr2['state'] = DISABLED
                        scnd_folder = filedialog.askdirectory(
                            initialdir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Screenshot'),
                            title='Open A File'
                        )
                        self.scndfoldername.insert(END, scnd_folder)
                        if scnd_folder and self.scndfoldername.get != '':
                            self.btn_cmpr2['state'] = NORMAL
                            self.scndfoldername['state'] = DISABLED
                            self.btn_cmpr2.config(command=lambda: self.compare_img(first_fldr, scnd_folder))
                        elif self.scndfoldername.get != '':
                            self.btn_cmpr2['state'] = DISABLED
                            self.foldername['state'] = NORMAL
                            self.foldername.delete(0, END)
                            messagebox.showerror("Error", "Please Select Source File")
                    except:
                        messagebox.showerror("Folder Issue", "Something went Wrong")

                self.btn_im2.config(command=scnd_fldr)
            elif self.foldername.get() == '':
                self.btn_cmpr2['state'] = DISABLED
                messagebox.showerror("Error", "Please Select Target File")
        except:
            messagebox.showerror("Folder Issue", "Something went Wrong")
            self.destroy()
            img_c()

    # Compare image files from both the folders
    def compare_img(self, first_fldr, scnd_folder):
        self.btn_cmpr2['state'] = DISABLED
        compare_img_folder(first_fldr, scnd_folder)
        self.foldername['state'] = NORMAL
        self.foldername.delete(0, END)
        self.scndfoldername['state'] = NORMAL
        self.scndfoldername.delete(0, END)
        self.btn_cmpr2['state'] = NORMAL
        self.destroy()
        img_c()


def compare_img_folder(first_fldr, scnd_folder):
    top = Toplevel()
    top.geometry("750x290+790+520")
    top.title("Compare Result {}".format(scnd_folder))
    top.resizable(False, False)
    top.focus()
    top_frame = Frame(top, height=340, bg="white")
    top_frame.pack(fill="both")
    treeview = ttk.Treeview(top_frame, selectmode='browse')
    treescrolly = ttk.Scrollbar(top_frame, orient="vertical", command=treeview.yview)
    treescrollx = ttk.Scrollbar(top_frame, orient="horizontal", command=treeview.xview)
    treeview.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
    treescrolly.pack(side="right", fill="y")
    treescrollx.pack(side="bottom", fill="x")

    treeview['columns'] = ("Image 1", "Image 2", "Result", "Location")
    treeview['show'] = 'headings'
    treeview.column("Image 1")
    treeview.column("Image 2")
    treeview.column("Result")
    treeview.column("Location")

    treeview.heading("Image 1", text="Target Image")
    treeview.heading("Image 2", text="Source Image")
    treeview.heading("Result", text="Result")
    treeview.heading("Location", text="Location")
    treeview.pack()
    try:
        path = Path(first_fldr)
        os.chdir(path)
        image_file = os.listdir()
        image_file_pngjpg = list()

        for x, z in enumerate(image_file):  # Sort out PNG and JPG files
            if z.endswith('.png') or z.endswith('.JPG'):
                image_file_pngjpg.append(z)

        path2 = Path(scnd_folder)
        os.chdir(path2)
        image_file1 = os.listdir()
        image_file1_pngjpg = list()
        for x, z in enumerate(image_file1):  # Sort out PNG and JPG files
            if z.endswith('.png') or z.endswith('.JPG'):
                image_file1_pngjpg.append(z)

        last_file = image_file[-1]
        list_diff = list()
        if len(image_file_pngjpg) == len(image_file1_pngjpg):
            current = str(datetime.datetime.now())  # Create a Compare Result Folder with date and time
            date, times = current.split()
            hour, minutes, seconds = times.split(":")
            name = first_fldr.split('/')
            save_file_name = name[-1]
            file = "Compare Result_" + save_file_name + " " + date + "_" + hour + "_" + minutes
            os.makedirs(file + "/Data")

            for i, j in zip(image_file_pngjpg, image_file1_pngjpg):
                if i.endswith('.png') or i.endswith('.JPG') and j.endswith('.png') or j.endswith('.JPG'):
                    image1 = cv2.imread(os.path.join(first_fldr, i))
                    image2 = cv2.imread(os.path.join(scnd_folder, j))
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
                        q = o_img_name + ".png"
                        save_loc = os.path.join(os.getcwd(), file)
                        data_loc = os.path.join(save_loc, "Data")
                        y = os.path.join(save_loc, z)
                        x = os.path.join(data_loc, q)
                        cv2.imwrite(y, image1)
                        cv2.imwrite(x, difference)
                        treeview.insert('', index="end", values=(i, j, "Difference", scnd_folder))
                        if i == last_file:
                            messagebox.showinfo("Completed", r"File is stored at {}/{} "
                                                             "\nResult is based on total {} files from Target Folder "
                                                             "and total {} files from Source Folder"
                                                .format(scnd_folder, file, len(image_file_pngjpg),
                                                        len(image_file1_pngjpg)))
                        continue
                    else:
                        treeview.insert("", index="end", values=(i, j, "No Difference", "None"))
                        if i == last_file and len(list_diff) != 0:
                            messagebox.showinfo("Completed",
                                                "File is stored at {}/Compare Result".format(scnd_folder))

                        elif i == last_file and len(list_diff) == 0:
                            messagebox.showinfo("Completed", "No difference occurred")
                            top.destroy()
                        continue
                else:
                    messagebox.showerror(".PNG or .JPG Files only",
                                         "Please make sure your folder contains '.png' and"
                                         " '.jpg' files only ")
                    top.destroy()
                    break
        else:
            messagebox.showerror("Folder Length does not match", "Total File in Target Folder is '{}' "
                                                                 "and Total Files in Source Folder is  '{}'"
                                 .format(len(image_file_pngjpg), len(image_file1_pngjpg)))
            top.destroy()
    except Exception as e:
        messagebox.showerror("Something went Wrong", "Please check : {}  ,'\nPossible Reasons of Failure"
                                                     "\n1.Make sure only jpg and png files are present in either of the"
                                                     " provided Location"
                                                     "\n2.The files would be created from different machines or it "
                                                     "could be taken from internet"
                                                     "\n3.If your reason is not mentioned contact developing team"
                             .format(e))
        top.destroy()


# Compare the two files
def compare_img_files(f, f1):
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

        else:
            messagebox.showinfo("Completed", "No difference Occur")
    except Exception as e:
        messagebox.showerror("Wrong files maybe", "Please Check {}" "\nPossible Reasons of Failure"
                                                  "\n1.The files would be created from different machines "
                                                  "or it could be taken from internet"
                                                  "\n2.Please select correct files or the image files of "
                                                  "same Size"
                                                  "\n3.If your reason is not mentioned contact developing "
                                                  "team".format(e))
