# -*- coding: utf-8 -*-
"""
This is a generic script for integratig into any type of data creation towards QR code generation.
The background image used is opensource and can be replaced with another.
"""

import tkinter
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import openpyxl

def enter_data():
    accepted = accept_var.get()
    
    if accepted == "Accepted":
        # User info
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()
        qroption = qroption_combobox.get()
        qrsize = qrsize_combobox.get()
        
        if firstname and lastname and qroption and qrsize:
            title = title_combobox.get()
            # Merchant info
            registration_status = reg_status_var.get()
            factory = factory_combobox.get()
            product = product_combobox.get()
            other = other_entry.get()
            
            print("First name: ", firstname, "Last name: ", lastname)
            print("Title: ", title)
            print("Factory Name: ", factory, "Product ID: ", product)
            print("Registration status", registration_status)
            print("Other: ", other)
            print("qroption: ", qroption, "qrsize:", qrsize)
            print("------------------------------------------")
            folder = "Output"
            if not os.path.exists(folder):
                os.makedirs(folder)
            filepath = "Output/dataQR.xlsx"
            if not os.path.exists(filepath):
                workbook = openpyxl.Workbook()
                sheet = workbook.active
                heading = ["First Name", "Last Name", "Title", 
                           "Warehouse", "Product ID" , "Registration status", "Other", "qroption", "qrsize"]
                sheet.append(heading)
                workbook.save(filepath)
            workbook = openpyxl.load_workbook(filepath)
            sheet = workbook.active
            sheet.append([firstname, lastname, title, factory, product, registration_status, other, qroption, qrsize])
            workbook.save(filepath)
                
        else:
            tkinter.messagebox.showwarning(title="Error", message="First name, Last name, QR Type & QR Size are required.")
    else:
        tkinter.messagebox.showwarning(title="Error", message="Please check all details are correct")

# Main window setup
window = tkinter.Tk()
window.title("Data Screener")

# Load the background image
background_image = Image.open("Image/background.jpg")
background_image = background_image.resize((600, 500))  # Resize as needed
background_photo = ImageTk.PhotoImage(background_image)

# Create a canvas to hold the background image
canvas = tkinter.Canvas(window, width=600, height=500)
canvas.pack(fill="both", expand=True)

# Set the background image on the canvas, aligning it to the right
canvas.create_image(600, 0, image=background_photo, anchor="ne")

# Frame to hold all widgets on top of the canvas
frame = tkinter.Frame(canvas, bg="white")
canvas.create_window(45, 250, window=frame, anchor="w")  # Align frame to the left side

# Saving User Info
user_info_frame = tkinter.LabelFrame(frame, text="User Information", bg="white")
user_info_frame.grid(row=0, column=0, padx=20, pady=10)

first_name_label = tkinter.Label(user_info_frame, text="First Name", bg="white")
first_name_label.grid(row=0, column=0)
last_name_label = tkinter.Label(user_info_frame, text="Last Name", bg="white")
last_name_label.grid(row=0, column=1)

first_name_entry = tkinter.Entry(user_info_frame)
last_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

title_label = tkinter.Label(user_info_frame, text="Title", bg="white")
title_combobox = ttk.Combobox(user_info_frame, values=["", "Mr.", "Ms.", "Dr.", "Other", "Prefer not to say"])
title_label.grid(row=0, column=2)
title_combobox.grid(row=1, column=2)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Saving Merchant info
merchant_frame = tkinter.LabelFrame(frame, text="Merchant Details", bg="white")
merchant_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

registered_label = tkinter.Label(merchant_frame, text="Registration Status", bg="white")
reg_status_var = tkinter.StringVar(value="Not Registered")
registered_check = tkinter.Checkbutton(merchant_frame, text="Currently Registered",
                                       variable=reg_status_var, onvalue="Registered", offvalue="Not registered",
                                       bg="white")

registered_label.grid(row=0, column=0)
registered_check.grid(row=0, column=1)

factory_label = tkinter.Label(merchant_frame, text="Factory Name", bg="white")
factory_combobox = ttk.Combobox(merchant_frame, values=["", "A", "B", "C", "Other"])
factory_label.grid(row=2, column=0)
factory_combobox.grid(row=3, column=0)

product_label = tkinter.Label(merchant_frame, text="Product ID", bg="white")
product_combobox = ttk.Combobox(merchant_frame, values=["ID1", "ID2", "ID3", 
                                                        "ID4", "ID5", "ID6", "Other"])
product_label.grid(row=2, column=1)
product_combobox.grid(row=3, column=1)

other_label = tkinter.Label(merchant_frame, text="Other", bg="white")
other_label.grid(row=2, column=3)
other_entry = tkinter.Entry(merchant_frame)
other_entry.grid(row=3, column=3)

qroption_label = tkinter.Label(merchant_frame, text="QR Type", bg="white")
qroption_combobox = ttk.Combobox(merchant_frame, values=["With Background", "Without Background"])
qroption_label.grid(row=4, column=0)
qroption_combobox.grid(row=5, column=0)

qrsize_label = tkinter.Label(merchant_frame, text="QR Size (in mm)", bg="white")
qrsize_combobox = ttk.Combobox(merchant_frame, values=["8.5", "25", "38", "45"])
qrsize_label.grid(row=4, column=1)
qrsize_combobox.grid(row=5, column=1)

for widget in merchant_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Accept terms
terms_frame = tkinter.LabelFrame(frame, text="All data is correct", bg="white")
terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

accept_var = tkinter.StringVar(value="Not Accepted")
terms_check = tkinter.Checkbutton(terms_frame, text="All the data is correct",
                                  variable=accept_var, onvalue="Accepted", offvalue="Not Accepted",
                                  bg="white")
terms_check.grid(row=0, column=0)

# Button
button = tkinter.Button(frame, text="Enter data", command=enter_data, bg="lightgray")
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)
 
window.mainloop()


