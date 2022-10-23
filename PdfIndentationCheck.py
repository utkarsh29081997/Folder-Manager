########################################################################################################################
# Author : Utkarsh Singh
# Project : Daily Utility
# Module : Checking the indentations and in short whole PDF
# Last Modified Date : 20 Dec,2020
########################################################################################################################
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import cv2
import os
import numpy as np
import MCPI
import datetime
import fitz


def pdf_indent_check():
    pdf_indent = pdf_indentation()


class pdf_indentation(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("780x390+790+120")
        self.title("Check PDF Indentation")
        self.resizable(False, False)
        self.focus_force()

        # Frame to hold top image
        self.first_frame = Frame(self, height=130, bg="white")
        self.first_frame.pack(fill='both')
        try:
            self.image_on_imgcmpr = PhotoImage(file=os.path.join(MCPI.path, 'Images/pdf-1.png'))
            self.label_photo = ttk.Label(self.first_frame, image=self.image_on_imgcmpr,
                                         background="white").place(x=50, y=30)
        except:
            pass
        self.label_top_heading = ttk.Label(self.first_frame, text="Check Indentations of your PDF",
                                           font=("Times New Roman", 15), background="white").place(x=190, y=40)

        self.pdfframe_bottom = Frame(self, height=500, bg='#8a211e')
        self.pdfframe_bottom.pack(fill='both')

        self.btn_pdf1 = ttk.Button(self.pdfframe_bottom, text="Target Folder", command=self.open_pdffile)
        self.btn_pdf1.place(x=670, y=70)
        self.btn_pdf2 = ttk.Button(self.pdfframe_bottom, text="Source Folder")
        self.btn_pdf2.place(x=670, y=150)

        self.pdf_file_name = ttk.Entry(self.pdfframe_bottom, width=80)
        self.pdf_file_name.place(x=10, y=70)

        self.scndpdf_file_name = ttk.Entry(self.pdfframe_bottom, width=80)
        self.scndpdf_file_name.place(x=10, y=150)

        self.btn_cmpr = ttk.Button(self.pdfframe_bottom, text="Compare")
        self.btn_cmpr.place(x=350, y=198)
        self.btn_cmpr['state'] = DISABLED

    def open_pdffile(self):
        try:
            # First File Location
            # Disabling the buttons once we get the locations of the file
            # Delete the Entry value i.e. location if one of the location remains empty and disable the compare button
            self.pdf_file_name['state'] = NORMAL
            self.pdf_file_name.delete(0, END)
            self.scndpdf_file_name['state'] = NORMAL
            self.scndpdf_file_name.delete(0, END)
            self.btn_cmpr['state'] = DISABLED
            filename = filedialog.askopenfilename(
                initialdir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Screenshot'),
                filetype=(("PDF files", "*.pdf"),),
                title='Open A File'
            )
            if filename:
                self.pdf_file_name.insert(END, filename)
                self.pdf_file_name['state'] = DISABLED

                # Second File Location
                def scn_file():
                    self.scndpdf_file_name['state'] = NORMAL
                    self.scndpdf_file_name.delete(0, END)
                    self.btn_cmpr['state'] = DISABLED
                    scndfilename = filedialog.askopenfilename(
                        initialdir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Screenshot'),
                        filetype=(("PDF files", "*.pdf"),),
                        title='Open A File'
                    )
                    if scndfilename:
                        self.scndpdf_file_name.insert(END, scndfilename)
                        self.scndpdf_file_name['state'] = DISABLED
                        self.btn_cmpr['state'] = NORMAL
                        self.btn_cmpr.config(command=lambda: compare_pdf_indent(filename, scndfilename))
                    elif self.scndpdf_file_name.get() == '':
                        self.btn_cmpr['state'] = DISABLED
                        self.pdf_file_name['state'] = NORMAL
                        self.pdf_file_name.delete(0, END)
                        messagebox.showerror("Error", "Please Select Source File")

                self.btn_pdf2.config(command=scn_file)
            elif self.pdf_file_name.get() == '':
                self.btn_cmpr['state'] = DISABLED
                messagebox.showerror("Error", "Please Select Target File")
                self.destroy()
                pdf_indent_check()

            def compare_pdf_indent(filename, scndfilename):
                check_indent_logic(filename, scndfilename)
                self.pdf_file_name['state'] = NORMAL
                self.pdf_file_name.delete(0, END)
                self.scndpdf_file_name['state'] = NORMAL
                self.scndpdf_file_name.delete(0, END)
                self.destroy()

        except Exception as e:
            messagebox.showerror("Something went wrong", "Please Check {} \nPossible Reasons of Failure"
                                                         "\n1.The files would be created from different machines "
                                                         "or it could be taken from internet"
                                                         "\n2.Please select correct files or the image files of "
                                                         "same Size"
                                                         "\n3.If your reason is not mentioned contact developing "
                                                         "team".format(e))
            self.destroy()


#    Extracting Each Page in Image format and then comparing both the images, The Image and Pic file are stored in same
#    dir. and these are images which is being used to compare and then the result is stored with the name of Page and
#    also the file has data folder which is to see the posi. of changes in the image and also it helps if the PDF
#    contains red color so it differentiate them
def check_indent_logic(filename, scndfilename):
    top = Toplevel()
    top.geometry("750x290+790+520")
    top.title("Compare Result {}".format(scndfilename))
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

    treeview.heading("Image 1", text="Target File")
    treeview.heading("Image 2", text="Source File")
    treeview.heading("Result", text="Result")
    treeview.heading("Location", text="Location")
    treeview.pack()

    doc = fitz.open(filename)
    doc2 = fitz.open(scndfilename)
    count = 0

    tem_image_loc = scndfilename.split('/')
    tem_image_loc.pop(-1)
    path = '/'.join(x for x in tem_image_loc)
    os.chdir(path)
    list_folder = os.listdir()
    if "Pdf_Indentation_Check_Result" not in list_folder:
        os.mkdir("Pdf_Indentation_Check_Result")
    elif "Pdf_Indentation_Check_Result" in list_folder:
        pass

    new_fldr = os.path.join(path, "Pdf_Indentation_Check_Result")
    os.chdir(new_fldr)
    total_page1 = doc.pageCount
    total_page2 = doc2.pageCount
    list_diff = list()
    if total_page1 == total_page2:
        current = str(datetime.datetime.now())  # Create a Extract PDF Indentetion to store Images Extracted from PDF's
        date, times = current.split()
        hour, minutes, seconds = times.split(":")

        new_fldr = "Pdf_Indentation_Check_Result" + " " + date + "_" + hour + "_" + minutes
        os.makedirs(new_fldr + "/Data")
        saving_result = os.path.join(os.getcwd(), new_fldr)
        os.chdir(saving_result)
        for page, pages in zip(doc, doc2):
            pix = page.getPixmap(alpha=False)
            pix2 = pages.getPixmap(alpha=False)
            count += 1
            pix.writePNG("Image.png")
            pix2.writePNG("Pic.png")
            image1 = cv2.imread("Image.png")
            image2 = cv2.imread("Pic.png")
            difference = cv2.subtract(image1, image2)
            result = not np.any(difference)
            diff_image = "Page_" + str(count)
            diff_posi_image = "Page_" + str(count) + ".png"
            diff_posi_image_loc = os.path.join(os.getcwd(), "Data")
            diff_posi_save = os.path.join(diff_posi_image_loc, diff_posi_image)
            if result is False:
                list_diff.append(count)
                # color the mask red
                Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
                ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
                difference[mask != 255] = [0, 170, 255]
                # add the red mask to the images to make the differences obvious
                image2[mask != 255] = [0, 0, 255]
                image1[mask != 255] = [0, 0, 255]
                cv2.imwrite(diff_image + ".png", image1)
                cv2.imwrite(diff_posi_save, difference)
                treeview.insert('', index="end", values=(diff_image, diff_image, "Difference", saving_result))
                if count == total_page2:
                    messagebox.showinfo("Completed", "All Files are Compared and the result is stored in "
                                                     "Pdf_Indentation_Check_Result/{} on your source Location "
                                        .format(new_fldr))
            else:
                treeview.insert('', index="end", values=(diff_image, diff_image, "No Difference", "None"))
                if count == total_page2 and len(list_diff) != 0:
                    messagebox.showinfo("Completed", "All Files are Compared and the result is stored in "
                                                     "Pdf_Indentation_Check_Result/{} on your source Location "
                                        .format(new_fldr))

                elif count == total_page2 and len(list_diff) == 0:
                    messagebox.showinfo("Completed", "No difference occurred")
                    top.destroy()
        os.remove("Image.png")
        os.remove("Pic.png")
        pdf_indentation()

    else:
        messagebox.showerror("File Length Not Same", "Pages are not equal total page in PDF 1 : {total_page1} "
                                                     "total pages in PDF 2 : {total_page2}")
        top.destroy()
