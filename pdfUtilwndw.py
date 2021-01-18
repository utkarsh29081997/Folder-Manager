################################################################
# Author : Utkarsh Singh
# Project : Daily Utility
# Module : Window to Hold PDF Utility Buttons
#          And windows for text and image compare
#          Also the logic of comparision and extract
# Last Modified Date : 29 Dec,2020
###############################################################
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import Utility_Launch
import os
import fitz
import difflib
import datetime
from Image_Compare import compare_img_folder
from PdfIndentationCheck import pdf_indent_check
from CommonTemplate import Comontemp


class pdf_util_window(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("450x450+720+120")
        self.title("PDF Utility")
        self.resizable(False, False)
        #  Top Frame to hold image and Label name
        self.pdficon_frame = Frame(self, height=120, bg="white")
        self.pdficon_frame.pack(fill="both")
        self.focus_force()
        try:
            self.pdfimage = PhotoImage(file=os.path.join(Utility_Launch.path, 'Image_01/PdfLogo.png'))
            self.pdfimage_icon = ttk.Label(self.pdficon_frame, image=self.pdfimage, background="white").place(x=50,
                                                                                                              y=30)
        except:
            pass
        self.pdf_label_heading = ttk.Label(self.pdficon_frame, text="PDF Operations", font=("Times New Roman", 15)
                                           , background="white").place(x=190, y=40)

        self.pdfframe_bottom = Frame(self, height=500, bg='#9e211c')
        self.pdfframe_bottom.pack(fill='both')

        self.pdf_util = ttk.Button(self.pdfframe_bottom, text='  Extract & Compare Text Content    ',
                                   command=lambda: Common_template(0))
        self.pdf_util.place(x=50, y=80)

        self.pdf_util = ttk.Button(self.pdfframe_bottom, text=' Extract & Compare Image Content  ',
                                   command=lambda: Common_template(1))
        self.pdf_util.place(x=50, y=130)

        self.pdf_util = ttk.Button(self.pdfframe_bottom, text=' Compare Indentations of PDF          ',
                                   command=pdf_indent_check)
        self.pdf_util.place(x=50, y=180)


# Common template to hold Text and Image Extraction and Compare Window objects
# Passing value through 'X' which will later be used to ssee if the user has clicked on what Operartions
class Common_template(Toplevel):
    def __init__(self, x):
        Toplevel.__init__(self)
        self.geometry("780x390+790+120")
        self.title("Check PDF Indentation")
        self.resizable(False, False)
        self.focus_force()

        list_ofImages = ['pdf.png', 'pdf_img.png']
        list_ofTopheading = ["Extract and Compare Text of Your PDF's", "Extract and Compare Images of Your PDF's"]
        list_ofColors = [['#204b85', '#5a2170'], ['#204b85', '#5a2170']]
        list_options = ["Text", "Images"]
        imagefile = 'Images/' + list_ofImages[x]

        self.pdfimgicon_frame = Frame(self, height=120, bg="white")
        self.pdfimgicon_frame.pack(fill="both")
        self.focus_force()
        # Frame to hold top image
        try:
            self.image_on_scrnshot = PhotoImage(file=os.path.join(Utility_Launch.path, imagefile))
            self.label_photo = ttk.Label(self.pdfimgicon_frame, image=self.image_on_scrnshot,
                                         background="white").place(x=50, y=30)
        except:
            pass
        self.label_top_heading = ttk.Label(self.pdfimgicon_frame, text=list_ofTopheading[x],
                                           font=("Times New Roman", 15)
                                           , background="white").place(x=190, y=40)

        # Two different tabs one for comparision through different folders and second for Single File Comparision
        self.tabcontrol = ttk.Notebook(self)
        self.tab1 = Frame(self.tabcontrol, bg=list_ofColors[x][0], height=500)
        self.tab1.pack(fill="both")
        self.tab2 = Frame(self.tabcontrol, bg=list_ofColors[x][1], height=500)
        self.tab2.pack(fill="both")

        # On File one for Folder by Folder Compare
        self.btn_pdf_tab1 = ttk.Button(self.tab1, text="PDF File", command=lambda: self.open_frstpdf_file(x))
        self.btn_pdf_tab1.place(x=670, y=70)

        # On Tab 2 for Single File Compare
        self.btn_pdf_tab2 = ttk.Button(self.tab2, text="Target File", command=lambda: self.open_pdf_files(x))
        self.btn_pdf_tab2.place(x=670, y=70)

        self.btn_pdf1_tab2 = ttk.Button(self.tab2, text="Source File")
        self.btn_pdf1_tab2.place(x=670, y=150)

        self.pdfname_tab1 = ttk.Entry(self.tab1, width=80)
        self.pdfname_tab1.place(x=10, y=70)

        self.pdfname_tab2 = ttk.Entry(self.tab2, width=80)
        self.pdfname_tab2.place(x=10, y=70)

        self.pdfname2_tab2 = ttk.Entry(self.tab2, width=80)
        self.pdfname2_tab2.place(x=10, y=150)

        self.tabcontrol.add(self.tab1, text=f"Extract {list_options[x]}")
        self.tabcontrol.add(self.tab2, text=f"Extract {list_options[x]} and Compare")
        self.tabcontrol.pack(fill='both')
        self.btn_cmpr = ttk.Button(self.tab2, text="Compare")
        self.btn_cmpr.place(x=350, y=190)
        self.btn_cmpr['state'] = DISABLED
        self.extract_txt = ttk.Button(self.tab1, text=f"Extract {list_options[x]}")
        self.extract_txt.place(x=350, y=190)

    def open_frstpdf_file(self, x):
        self.pdfname_tab1['state'] = NORMAL
        self.pdfname_tab1.delete(0, END)
        filename = filedialog.askopenfilename(
            initialdir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Screenshot'),
            filetype=(("PDF files", '*.pdf'),),
            title='Open A File'
        )
        if filename:
            self.pdfname_tab1.insert(END, filename)
            self.pdfname_tab1['state'] = DISABLED
            if x == 0:
                self.extract_txt.config(command=lambda: extract_textfrom_pdf(filename))
            else:
                self.extract_txt.config(command=lambda: extract_images(filename))

    def open_pdf_files(self, x):
        try:
            # Disabling the buttons once we get the locations of the file
            # Delete the Entry value i.e. location if one of the location remains empty and disable the compare button
            self.pdfname_tab2['state'] = NORMAL
            self.pdfname_tab2.delete(0, END)
            self.pdfname2_tab2['state'] = NORMAL
            self.pdfname2_tab2.delete(0, END)
            self.btn_cmpr['state'] = DISABLED
            filename = filedialog.askopenfilename(
                initialdir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Screenshot'),
                filetype=(("PDF files", '*.pdf'),),
                title='Open A File'
            )
            self.pdfname_tab2.insert(END, filename)
            if filename and self.pdfname_tab2.get() != "":
                self.pdfname_tab2['state'] = DISABLED

                def open_pdf2_files():
                    self.pdfname2_tab2['state'] = NORMAL
                    self.pdfname2_tab2.delete(0, END)
                    self.btn_cmpr['state'] = DISABLED
                    scnd_filename = filedialog.askopenfilename(
                        initialdir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Screenshot'),
                        filetype=(("PDF files", '*.pdf'),),
                        title='Open A File'
                    )
                    self.pdfname2_tab2.insert(END, scnd_filename)
                    if scnd_filename and self.pdfname2_tab2.get():
                        self.pdfname2_tab2['state'] = DISABLED
                        self.btn_cmpr['state'] = NORMAL
                        if x == 0:
                            self.btn_cmpr.config(command=lambda: self.compare_pdf_btn_cnfg(filename, scnd_filename))
                        else:
                            self.btn_cmpr.config(command=lambda: self.compare_pdfimg_btn_cnfg(filename, scnd_filename))
                    elif self.pdfname2_tab2.get() == "":
                        self.btn_cmpr['state'] = DISABLED
                        self.pdfname_tab2['state'] = NORMAL
                        self.pdfname_tab2.delete(0, END)
                        messagebox.showerror("Error", "Please Select Source File")

                self.btn_pdf1_tab2.config(command=open_pdf2_files)
            elif self.pdfname_tab2.get() == "":
                self.btn_cmpr['state'] = DISABLED
                messagebox.showerror("Error", "Please Select Target File")
        except Exception as e:
            messagebox.showerror("Error", "Something Went Wrong \n{}".format(e))

    def compare_pdf_btn_cnfg(self, filename, scnd_filename):
        self.btn_cmpr['state'] = DISABLED
        compare_pdf_text(filename, scnd_filename)
        self.pdfname_tab2['state'] = NORMAL
        self.pdfname_tab2.delete(0, END)
        self.pdfname2_tab2['state'] = NORMAL
        self.pdfname2_tab2.delete(0, END)
        self.btn_cmpr['state'] = NORMAL
        self.destroy()
        Common_template(0)

    def compare_pdfimg_btn_cnfg(self, filename, scnd_filename):
        self.btn_cmpr['state'] = DISABLED
        # Passing filename's (Location) to extract Images from the PDF's and from the method we're returning the
        # location in order to pass the location to the Image_compare
        z = extract_images(filename)
        path = os.path.join(filename, z)
        path = path.replace(os.sep, '/')
        y = extract_images(scnd_filename)
        path0 = os.path.join(filename, y)
        path0 = path0.replace(os.sep, '/')
        compare_img_folder(path, path0)
        self.pdfname_tab2['state'] = NORMAL
        self.pdfname_tab2.delete(0, END)
        self.pdfname2_tab2['state'] = NORMAL
        self.pdfname2_tab2.delete(0, END)
        self.btn_cmpr['state'] = NORMAL
        self.destroy()
        Common_template(1)


# Compare Extracted text and save the result in Html format
def compare_pdf_text(filename, scnd_filename):
    filepath = filename
    filepath2 = scnd_filename

    current = str(datetime.datetime.now())  # Create a Extract Image Folder to store Images Extracted from PDF's
    date, times = current.split()
    hour, minutes, seconds = times.split(":")

    file_extract = filename
    file_name, ext = os.path.splitext(file_extract)
    name = file_name.split('/')
    save_txt_filename = name[-1]
    html_file = save_txt_filename + " " + date + "_" + hour + "_" + minutes + '.html'
    save_txt_filename = save_txt_filename + " " + date + "_" + hour + "_" + minutes + '.txt'

    file_extractscnpdf = scnd_filename
    file_namescnd, extn = os.path.splitext(file_extractscnpdf)
    namescnd = file_namescnd.split('/')
    save_scndtxt_filename = namescnd[-1]
    save_scndtxt_filename = save_scndtxt_filename + " " + date + "_" + hour + "_" + minutes + '.txt'
    path = namescnd.pop(-1)
    path = '/'.join(x for x in namescnd)
    text = ''
    text2 = ''
    os.chdir(path)
    folders_in_loc = os.listdir()
    if "Compared Text" not in folders_in_loc:
        os.mkdir("Compared Text")
    elif "Compared Text" in folders_in_loc:
        pass
    if "Extracted Text" not in folders_in_loc:
        os.mkdir("Extracted Text")
    elif "Extracted Text" in folders_in_loc:
        pass
    new_fldr = os.path.join(path, "Compared Text")
    ext_txt_fldr = os.path.join(path, "Extracted Text")
    with open(os.path.join(ext_txt_fldr, save_txt_filename), 'w', encoding="utf-8") as randm:
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.getText()
        randm.write(text)

    with open(os.path.join(ext_txt_fldr, save_scndtxt_filename), 'w', encoding="utf-8") as randm0:
        with fitz.open(filepath2) as doc2:
            for page in doc2:
                text2 += page.getText()
        randm0.write(text2)

    with open(os.path.join(ext_txt_fldr, save_txt_filename), 'r', encoding='utf-8') as fileread:
        f = fileread.readlines()
        with open(os.path.join(ext_txt_fldr, save_scndtxt_filename), 'r', encoding='utf-8') as tofileread:
            t = tofileread.readlines()
            with open(os.path.join(new_fldr, html_file), 'w', encoding='utf-8') as diff_report:
                diff = difflib.HtmlDiff().make_file(f, t, filepath, filepath2)
                diff_report.write(diff)
    messagebox.showinfo("Successful comparison", "Your Files are compared and stored at \n"
                                                 "1. Target File : {} \n"
                                                 "2. Source File : {} \n"
                                                 "3. Compared Report : {}".format(os.path.join(path, save_txt_filename),
                                                                                  os.path.join(path,
                                                                                               save_scndtxt_filename)
                                                                                  , os.path.join(path, html_file)))


# Extract Text from PDF Logic
def extract_textfrom_pdf(filename):
    try:
        if filename:
            file_extract = filename

            current = str(datetime.datetime.now())  # Create a Extract Image Folder to store Images Extracted from PDF's
            date, times = current.split()
            hour, minutes, seconds = times.split(":")

            file_name, ext = os.path.splitext(file_extract)
            name = file_name.split('/')
            save_txt_filename = name[-1]
            save_txt_filename = save_txt_filename + " " + date + "_" + hour + "_" + minutes + '.txt'
            name.pop(-1)
            path = '/'.join(x for x in name)
            os.chdir(path)
            text = ''
            list_folder = os.listdir()
            if "Extracted Text" not in list_folder:
                os.mkdir("Extracted Text")
            elif "Extracted Text" in list_folder:
                pass
            new_fldr = os.path.join(path, "Extracted Text")
            with open(os.path.join(new_fldr, save_txt_filename + '.txt'), 'w', encoding='utf-8')as fileext:
                with fitz.open(filename) as doc:
                    for page in doc:
                        text += page.getText()
                fileext.write(text)
            messagebox.showinfo("Completed", "Text from PDF is extracted and stored at below location \n"
                                             r"{}\Extracted Text\{}.txt".format(os.getcwd(), save_txt_filename))
    except Exception as e:
        messagebox.showerror("Error", "Something Went Wrong \n{}".format(e))

# Extract Image from PDF Logic
def extract_images(filename):
    global count, folder_name
    filepath = filename
    try:
        if filename:
            file_extract = filename
            file_name, ext = os.path.splitext(file_extract)
            name = file_name.split('/')
            save_txt_filename = name[-1]  # Name of the  PDF File
            current = str(datetime.datetime.now())  # Create a Extract Image Folder to store Images Extracted from PDF's
            date, times = current.split()
            hour, minutes, seconds = times.split(":")
            folder_name = "Extracted Images from " + save_txt_filename + " " + date + "_" + hour + "_" + minutes
            name.pop(-1)
            path = '/'.join(x for x in name)
            os.chdir(path)
            os.mkdir(folder_name)
            count = 0
        with fitz.open(filepath) as doc:
            for i in range(len(doc)):
                for img in doc.getPageImageList(i):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    count += 1
                    page = i
                    img_name = "Page" + str(page) + "_" + str(count) + ".png"
                    save_loc = os.path.join(folder_name, img_name)
                    if pix.n < 5:  # this is GRAY or RGB
                        pix.writePNG(save_loc)
                    else:  # CMYK: convert to RGB first
                        pix1 = fitz.Pixmap(fitz.csRGB, pix)
                        pix1.writePNG(save_loc)
            messagebox.showinfo("Completed", "Images inside PDF are extracted and stored at below location \n "
                                             "{}\{}".format(os.getcwd(), folder_name))
            filename = os.path.join(os.getcwd(), folder_name)
            return filename
    except Exception as e:
        messagebox.showerror("Error", "Something Went Wrong : {}".format(e))
