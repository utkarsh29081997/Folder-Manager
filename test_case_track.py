import datetime
import os
from tkinter import messagebox


from scrnshot_wndw import scrnshot


def track_test(test_name):
    # creating a directory inside Hands-on to
    global making_dir
    # get Test Case name from user
    test_case = test_name

    # Saving the New directory with the date hour and min.
    # Using Try except so if same folder exist user will get pop up to change the folder name
    current = str(datetime.datetime.now())
    date, times = current.split()
    hour, minutes, seconds = times.split(":")
    directory = date + "_" + hour + "_" + minutes
    try:
        making_dir = str(directory) + ' ' + test_case
        os.makedirs(making_dir + "/Images")
        os.chdir(os.path.join(os.getcwd(), making_dir))
        imgfldrpath = os.path.join(os.getcwd(), 'Images')
        scrnshot(imgfldrpath)
    except:
        msg = "{} Exist..Please try adding some numbers to your folder name ".format(making_dir)
        messagebox.showerror("Error", msg, icon='error')
