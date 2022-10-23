################################################################
# Author : Utkarsh Singh
# Project : Daily Utility
# Module :  Main Window / Top Window
# Last Modified Date : 07 Mar,2021
###############################################################
import app_wndw
from stand_alone_tc_wndw import tc_window
from tkinter import ttk
import time
import Excel_utility
import Image_Compare
from pdfUtilwndw import pdf_util_window
from tkinter import *
from tkinter.tix import *


def main():
    root = Tk()
    root.geometry("600x600+120+120")
    root.title("MCPI")
    root.resizable(False, False)
    root.lift()
    frst = first_frame(root)
    root.mainloop()


def create_tc_wndw(event):
    Tc = tc_window()


def create_app_wndw(event):
    App = app_wndw.app_window()


def excel_util(event):
    exc = Excel_utility.excel_util()


def img_cmpr(event):
    img_c = Image_Compare.image_compare()


def pdf_util_launch(event):
    pdf_util = pdf_util_window()


# First Root file to call other class
# I have used ttk and tk components within this class to makes sure the design looks good and bindded the buttons
# with the two functions created outside the class
path = os.getcwd()


class first_frame(object):
    def __init__(self, master):
        self.master = master

        #  Top Frame to hold image and Label name
        self.icon_frame = Frame(master, height=120, bg="white")
        self.icon_frame.pack(fill="both")
        self.icon_frame.focus_force()
        self.image = PhotoImage(file=os.path.join(path, 'Images/icon.png'))
        self.label_photo = ttk.Label(self.icon_frame, image=self.image, background="white").place(x=30, y=30)
        self.label_heading = ttk.Label(self.icon_frame, text="Daily Use", font=("Times New Roman", 15)
                                       , background="white").place(x=190, y=40)
        self.label_sub_head = ttk.Label(self.icon_frame, text="use to ease work.", font=("Times New Roman", 10),
                                        background="white").place(x=190, y=80)
        self.label_date = Label(self.icon_frame, bg="white", text=time.strftime("%a. %d. %b,%Y"),
                                width=20, font=("Times New Roman", 11))
        self.label_date.place(x=415, y=10)

        self.label_time = Label(self.icon_frame, bg="white", width=12,font=("Times New Roman", 11))
        self.label_time.place(x=490, y=34)
        self.clock()

        # Bottom Frame to hold  buttons
        self.tip = Balloon()
        self.frame_bottom = Frame(master, height=500, bg='#22303C')
        self.frame_bottom.pack(fill='both')
        self.create_btn = ttk.Button(self.frame_bottom, text=' Application Folder  ',
                                     command=lambda: create_app_wndw(None))

        self.btn_img1 = PhotoImage(file=os.path.join(path, 'Images/folder-1.png'))
        self.btn_lbl1 = ttk.Label(self.frame_bottom, image=self.btn_img1, background='#22303C').place(x=29, y=100)

        # Passing Enter Key
        self.create_btn.bind("<Return>", create_app_wndw)
        self.create_btn.place(x=90, y=100)

        self.tip.bind_widget(self.create_btn, balloonmsg="Create Application Folder and Test Case")
        self.tip.subwidget('label').forget()

        # Test Case Folder Button
        self.create_test_case = ttk.Button(self.frame_bottom, text=' Test Case Folder      ',
                                           command=lambda: create_tc_wndw(None))

        self.btn_img2 = PhotoImage(file=os.path.join(path, 'Images/online-learning.png'))
        self.btn_lbl2 = ttk.Label(self.frame_bottom, image=self.btn_img2, background='#22303C').place(x=29, y=170)

        self.create_test_case.bind("<Return>", create_tc_wndw)
        self.create_test_case.place(x=90, y=170)

        self.tip.bind_widget(self.create_test_case, balloonmsg="Create Test Case Folder/Pick where you left")
        self.tip.subwidget('label').forget()

        # Excel Working
        self.work_excel = ttk.Button(self.frame_bottom, text=' Work with Excel       ',
                                     command=lambda: excel_util(None))

        self.btn_img3 = PhotoImage(file=os.path.join(path, 'Images/xls.png'))
        self.btn_lbl3 = ttk.Label(self.frame_bottom, image=self.btn_img3, background='#22303C').place(x=29, y=240)

        self.work_excel.bind("<Return>", excel_util)
        self.work_excel.place(x=90, y=240)

        self.tip.bind_widget(self.work_excel, balloonmsg="Modify your Excel Report Sheet ")
        self.tip.subwidget('label').forget()

        # Image Compare Button
        self.img_cmpr = ttk.Button(self.frame_bottom, text=' Image Compare      ',
                                   command=lambda: img_cmpr(None))
        self.btn_img4 = PhotoImage(file=os.path.join(path, 'Images/compare.png'))
        self.btn_lbl4 = ttk.Label(self.frame_bottom, image=self.btn_img4, background='#22303C').place(x=29, y=310)

        self.img_cmpr.bind("<Return>", img_cmpr)
        self.img_cmpr.place(x=90, y=310)

        self.tip.bind_widget(self.img_cmpr, balloonmsg="Compare Single/Multiple Images")
        self.tip.subwidget('label').forget()

        # PDF Utility Button
        self.pdf_util = ttk.Button(self.frame_bottom, text='  PDF  Utility              ',
                                   command=lambda: pdf_util_launch(None))

        self.btn_img5 = PhotoImage(file=os.path.join(path, 'Images/pdf-1 (3).png'))
        self.btn_lbl5 = ttk.Label(self.frame_bottom, image=self.btn_img5, background='#22303C ').place(x=29, y=380)

        self.pdf_util.bind("<Return>", pdf_util_launch)
        self.pdf_util.place(x=90, y=380)

        self.tip.bind_widget(self.pdf_util, balloonmsg="Operations On a PDF")
        self.tip.subwidget('label').forget()

        self.footerlabel = Label(self.frame_bottom, bg='white', fg='black', bd=2, width=75,
                                 text="©MCPI", relief=SUNKEN, anchor=CENTER).place(x=0, y=455)

    def clock(self):
        curr_time = time.strftime('%H:%M:%S')
        self.label_time.config(text=curr_time)
        self.label_time.after(1000, self.clock)


if __name__ == '__main__':
    main()
