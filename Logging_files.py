########################################################################################################################
# Author : Utkarsh Singh
# Project : Daily Utility
# Module : Program to log in Excel sheet whether defect exist or not if exist then take defect _id and other details and
#          log them in excel sheet as well
########################################################################################################################

import openpyxl
import os
import CheckDirectory
import datetime
from openpyxl import Workbook
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import Utility_Launch


class defect_info(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("550x550+790+120")
        self.title("Defect Info")
        self.resizable(False, False)

        # Top Frame for icon and name
        self.frame_on_defect_info = Frame(self, height=120, bg="white")
        self.frame_on_defect_info.pack(fill="both")
        try:
            self.frame_defect_info = PhotoImage(file=os.path.join(Utility_Launch.path, 'Image_01/package.png'))
            self.label_photo = ttk.Label(self.frame_on_defect_info, image=self.frame_defect_info,
                                         background="white").place(x=30, y=30)
        except:
            pass
        self.label_heading = ttk.Label(self.frame_on_defect_info, text="Defect Info.!!!", font=("Times New Roman", 15)
                                       , background="white").place(x=190, y=40)

        # Bottom frame to hold defect info
        self.btm_defectinfo_frame = Frame(self, height=900, bg='#50946a').pack(fill='both')
        self.defect_info_label = ttk.Label(self, text="Enter Defect ID : ", font=("Times New Roman", 12)
                                           , background="#50946a").place(x=10, y=180)
        self.defect_id_entry = ttk.Entry(self, width=15)
        self.defect_id_entry.place(x=180, y=180)
        self.defect_id_entry.focus_force()

        self.defect_desc_label = ttk.Label(self, text="Short Desc. : ", font=("Times New Roman", 12)
                                           , background="#50946a").place(x=10, y=220)
        self.label_example = ttk.Label(self.frame_on_defect_info, text="(eg. Server error,Fatal error,etc.)"
                                       , font=("Times New Roman", 12), background="white").place(x=10, y=240)
        self.defect_desc_entry = ttk.Entry(self, width=15)
        self.defect_desc_entry.place(x=180, y=220)

        self.defect_scrn_label = ttk.Label(self, text="Screen Name : ", font=("Times New Roman", 12)
                                           , background="#50946a").place(x=10, y=270)
        self.defect_scrn_entry = ttk.Entry(self, width=15)
        self.defect_scrn_entry.place(x=180, y=270)

        self.defect_info_done = ttk.Button(self, width=14, text='DONE'
                                           , command=self.close_wndw)

        self.defect_info_done.place(x=180, y=320)

    def close_wndw(self):
        d_id = self.defect_id_entry.get()
        d_des = self.defect_desc_entry.get()
        d_scrn = self.defect_scrn_entry.get()
        if d_id and d_des and d_scrn != ' ':
            log_in_excel(os.getcwd(), d_id, d_des, d_scrn)
            self.destroy()
        else:
            messagebox.showerror("Error!", "Please Fill all the mandatory fields", icon="error")


# def create_fldr():
#     old_dir = os.getcwd()
#     CheckDirectory.check_directory()
#     list_of_fldr = os.listdir()
#     if "My Reports" not in list_of_fldr:
#         os.mkdir("My Reports")
#         log_in_excel(old_dir,None,None,None)
#     elif "My Reports" in list_of_fldr:
#         log_in_excel(old_dir,None,None,None)


def log_in_excel(old_dir, defect_id, defect_desc, defect_sc):
    CheckDirectory.check_directory()
    list_of_fldr = os.listdir()
    if "My Reports" not in list_of_fldr:
        os.mkdir("My Reports")
    d_id = defect_id
    d_sc = defect_desc
    d_des = defect_sc
    loc = old_dir
    old_dir = old_dir.split("\\")
    wb_name = old_dir[-4]
    app_name = old_dir[-3]
    tc_name = old_dir[-2]
    date = datetime.date.today()
    if "Defect" in old_dir:
        status = 'Fail'
    else:
        status = 'Pass'
    os.chdir(os.path.join(os.getcwd(), "My Reports"))
    # Check weather the file exist or not
    list_of_wb = list()
    prsnt_wb = os.listdir()
    for x in prsnt_wb:
        wb_name_prsnt, extn = os.path.splitext(x)
        list_of_wb.append(wb_name_prsnt)

    # If file does Not exist Create
    file_name = wb_name + ".xlsx"
    if wb_name not in list_of_wb:
        wb = Workbook()
        sheet = wb.active
        sheet.title = wb_name
        data = [('App. Name', 'Test Case', 'Date', 'Status', 'Location', 'Defect Id', 'Short Desc.', 'Screen Name'),
                (app_name, tc_name, date, status, loc, d_id, d_sc, d_des)
                ]

        for row in data:
            sheet.append(row)
        wb.save(file_name)
    # If file exist enter the details
    elif wb_name in list_of_wb:
        try:
            wb = openpyxl.load_workbook(file_name)
            act_sheet = wb.active
            act_sheet.append([app_name, tc_name, date, status, loc, d_id, d_sc, d_des])
            wb.save(file_name)
        except:
            messagebox.showerror("Error!", "Please close the {}.xlsx File".format(wb_name))
